from fastapi import APIRouter, Response
from sqlalchemy.exc import NoResultFound

from app.dependencies import DBDep, UserIdDep, UserTokenDep
from app.exceptions import UserAlreadyExistsException, UserEmailAlreadyExistsHTTPException, EmailNotCorrectException, \
    EmailNotCorrectHTTPException, UserNotEnoughRightsException, UserNotEnoughRightsHTTPException, \
    EmailNotRegisteredException, EmailNotRegisteredHTTPException, IncorrectPasswordException, \
    IncorrectPasswordHTTPException, UserNotFoundException, UserNotFoundHTTPException, UserNotAdminException, \
    UserNotAdminHTTPException
from app.schemas.users import UserPATCH, UserUpdate, UserRequestAdd, UserEnter
from app.services.auth import AuthService

router = APIRouter(prefix="/admin", tags=["Админ-эндпоинты"])

@router.post("/register", summary="Создать пользователя", description="Регистрация пользователей в системе")
async def register_user(db: DBDep, data: UserRequestAdd):
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
        raise UserEmailAlreadyExistsHTTPException
    except EmailNotCorrectException:
        raise EmailNotCorrectHTTPException

    return "Пользователь успешно зарегистрирован"

@router.post("/login", summary="Войти в систему", description="Введите email и пароль")
async def login_user(db: DBDep, data: UserEnter, response: Response):
    try:
        access_token = await AuthService(db).login_admin(data)
    except UserNotEnoughRightsException:
        raise UserNotEnoughRightsHTTPException
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
    except NoResultFound:
        raise EmailNotRegisteredHTTPException
    except UserNotAdminException:
        raise UserNotAdminHTTPException

    response.set_cookie("access_token", access_token)
    return "Вы успешно вошли в систему"

@router.get("/{user_id}/user_info", summary="Получить информацию о пользователе")
async def get_me(db: DBDep, user_id: UserIdDep, user_token: UserTokenDep):
    try:
        if user_token:
            return await AuthService(db).get_me(user_id)
        else:
            raise UserNotEnoughRightsHTTPException
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    except UserNotEnoughRightsException:
        raise UserNotEnoughRightsHTTPException


@router.get("/users", summary="Получить информацию о пользователях",
            description="Информация обо всех пользователях, зарегистрированных в системе")
async def get_users(db: DBDep, user_token: UserTokenDep):
    try:
        if user_token:
            return await AuthService(db).get_all()
        else:
            raise UserNotEnoughRightsHTTPException
    except NoResultFound:
        raise UserNotFoundException


@router.put("/users/update_user", summary="Полное обновление информации о пользователе",
            description="Обновление всех полей пользователя")
async def update_user(db: DBDep, user_id: int, user_data: UserUpdate, user_token: UserTokenDep):
    try:
        if user_token:
            await AuthService(db).update_user(user_id, user_data)
            return "Пользователь обновлен"
        else:
            raise UserNotEnoughRightsHTTPException
    except UserNotFoundException:
        raise UserNotFoundHTTPException


@router.patch("/users/{user_id}", summary="Частичное обновление информации о пользователе",
              description="Можно обновить лишь необходимиые поля у пользователя")
async def partial_update_user(db: DBDep, user_id: int, user_data: UserPATCH, user_token: UserTokenDep):
    try:
        if user_token:
            await AuthService(db).partial_update_user(user_id, user_data)
            return "Пользователь успешно обновлен"
        else:
            raise UserNotEnoughRightsHTTPException
    except UserAlreadyExistsException:
        raise UserEmailAlreadyExistsHTTPException
    except UserNotFoundException:
        raise UserNotFoundHTTPException

@router.delete("", summary="Удаление пользователя из системы",
               description="Удаление пользователя по его id")
async def delete_user(db: DBDep, user_id: int, user_token: UserTokenDep):
    try:
        if user_token:
            await AuthService(db).delete_user(user_id)
            return "Пользователь успешно удален"
        else:
            raise UserNotEnoughRightsHTTPException
    except UserNotFoundException:
        raise UserNotFoundHTTPException


@router.post("/logout", summary="Выйти из системы")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return "Вы успешно вышли из системы"