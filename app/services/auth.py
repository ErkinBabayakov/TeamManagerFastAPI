
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Response, Request
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError, NoResultFound

from app.config import settings
from app.exceptions import ObjectAlreadyExistsException, UserAlreadyExistsException, UserNotEnoughRightsException, \
    EmailNotRegisteredException, IncorrectPasswordException, ObjectNotFoundException, UserNotFoundException, \
    EmailNotRegisteredHTTPException, UserNotManagerOrAdminException
from app.schemas.users import UserAdd, UserRequestAdd, UserEnter, UserUpdate, UserUpdateWithHashPassword, UserPATCH, \
    UserPATCHUpdateWithHashPassword, UserPATCHUpdateWithoutHashPassword, UserDelete, User, UserRole
from app.services.base import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Неверный токен")


    async def register_user(self, user_data: UserRequestAdd):
        hashed_password = self.hash_password(user_data.password)
        new_user_data = UserAdd(
            email=user_data.email,
            hashed_password=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            role=user_data.role,
        )
        try:
            await self.db.users.add(new_user_data)
            await self.db.commit()
        except ObjectAlreadyExistsException as ex:
            raise UserAlreadyExistsException from ex

    async def login_admin(self, user_data: UserEnter):

        user = await self.db.users.get_user_with_hashed_password(email=user_data.email)
        if not user:
            raise EmailNotRegisteredException
        user_admin = await self.db.users.check_verify_admin_user(user_id=user.id)
        if user_admin.role != UserRole.admin:
            raise UserNotEnoughRightsException
        if not self.verify_password(user_data.password, user.hashed_password):
            raise IncorrectPasswordException
        access_token = AuthService().create_access_token({"user_id": user.id, "first_name": user.first_name,
                                                          "last_name": user.last_name, "role": user.role})
        return access_token

    async def login_manager(self, user_data: UserEnter):
        user = await self.db.users.get_user_with_hashed_password(email=user_data.email)
        if not user:
            raise EmailNotRegisteredException
        user_manager = await self.db.users.check_verify_admin_user(user_id=user.id)
        if user_manager.role.manager != UserRole.manager or user_manager.role.admin != UserRole.admin:
            raise UserNotManagerOrAdminException
        if not self.verify_password(user_data.password, user.hashed_password):
            raise IncorrectPasswordException
        access_token = AuthService().create_access_token({"user_id": user.id, "first_name": user.first_name,
                                                          "last_name": user.last_name, "role": user.role})
        return access_token

    async def login_user(self, user_data: UserEnter):
        try:
            user = await self.db.users.get_user_with_hashed_password(email=user_data.email)
            if not user:
                raise EmailNotRegisteredException
            if not self.verify_password(user_data.password, user.hashed_password):
                raise IncorrectPasswordException
            access_token = AuthService().create_access_token({"user_id": user.id, "first_name": user.first_name,
                                                              "last_name": user.last_name, "role": user.role})
            return access_token
        except NoResultFound:
            raise EmailNotRegisteredHTTPException

    async def get_me(self, user_id: int):
        try:
            user = await self.db.users.get_one(id=user_id)
            return user
        except ObjectNotFoundException as ex:
            raise UserNotFoundException from ex

    async def get_all(self):
        try:
            return await self.db.users.get_all()
        except ObjectNotFoundException as ex:
            raise UserNotFoundException from ex

    async def update_user(self, user_id: int, user_data: UserUpdate):
        try:
            existing_user = await self.get_me(user_id)
            if not existing_user:
                raise UserNotFoundException

            hashed_password = self.hash_password(user_data.password)
            updated_user_data_password = UserUpdateWithHashPassword(
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                hashed_password=hashed_password,
                role=user_data.role,
            )
            updated_user = await self.db.users.edit(
                updated_user_data_password, id=user_id, exclude_unset=True, exclude_none=True
            )
            await self.db.commit()
            return updated_user
        except IntegrityError as ex:
            raise UserAlreadyExistsException from ex

    async def partial_update_user(self, user_id: int, user_data: UserPATCH):
        try:
            existing_user = await self.get_me(user_id)
            if not existing_user:
                raise UserNotFoundException

            if user_data.password is not None:
                hashed_password = self.hash_password(user_data.password)
                updated_user_data_password = UserPATCHUpdateWithHashPassword(
                    hashed_password=hashed_password,
                    first_name=user_data.first_name,
                    last_name=user_data.last_name,
                    role=user_data.role,
                )
                updated_user = await self.db.users.edit(
                    updated_user_data_password, id=user_id, exclude_unset=True, exclude_none=True
                )
                await self.db.commit()
                return updated_user

            updated_user_without_hashed_password = UserPATCHUpdateWithoutHashPassword(
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                role=user_data.role,
            )
            updated_user = await self.db.users.edit(
                updated_user_without_hashed_password, id=user_id, exclude_unset=True, exclude_none=True,
            )
            await self.db.commit()
            return updated_user

        except IntegrityError as ex:
            raise UserAlreadyExistsException from ex

    async def delete_user(self, user_id: int):
        try:
            query_verify_admin = await self.db.users.check_verify_admin_user(user_id=user_id)
            if query_verify_admin.role != UserRole.admin:
                raise UserNotEnoughRightsException
            await self.db.users.delete(user_id=user_id)
            await self.db.commit()

        except IntegrityError as ex:
            raise UserNotFoundException from ex

    async def get_current_user(self, user_id: int):
        existing_user = await self.get_me(user_id)
        existing_user_with_user_id = existing_user.model_dump().get("user_id")
        if existing_user_with_user_id != user_id:
            raise UserNotEnoughRightsException
        return existing_user_with_user_id




