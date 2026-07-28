from pydantic import EmailStr
from sqlalchemy import select, or_
from sqlalchemy.exc import NoResultFound

from app.exceptions import UserNotEnoughRightsException, UserNotManagerOrAdminException
from app.models import UserOrm
from app.repositories.base import BaseRepository
from app.repositories.mappers.mappers import UserDataMapper
from app.schemas.users import User, UserWithHashPassword, UserAdd, UserCheckAdmin


class UserRepository(BaseRepository):
    model = UserOrm
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UserWithHashPassword.model_validate(model)

    async def check_verify_admin_user(self, user_id: int):
        try:
            query = select(self.model).where(
                self.model.id == user_id,
                or_(self.model.role == "admin", self.model.role == "manager")
            )
            result = await self.session.execute(query)
            model = result.scalars().one()
            return UserCheckAdmin.model_validate(model)
        except NoResultFound as ex:
            raise  UserNotManagerOrAdminException from ex






