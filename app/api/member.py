from fastapi import APIRouter, Response, Request
from jwt.exceptions import ExpiredSignatureError
from app.dependencies import DBDep
from app.exceptions import UserNotFoundException, UserNotFoundHTTPException, UserNotEnoughRightsException, \
    UserNotEnoughRightsHTTPException, TokenExpiredHTTPException, EmailNotRegisteredException, \
    EmailNotRegisteredHTTPException, IncorrectPasswordException, IncorrectPasswordHTTPException, TaskNotFoundException, \
    TaskNotFoundHTTPException
from app.schemas.users import  UserEnter
from app.services.auth import AuthService
from app.services.tasks import TaskService

router = APIRouter(prefix="/member", tags=["Эндпоинты сотрудников"])


@router.post("/login", summary="Войти в систему", description="Введите email и пароль")
async def login_user(db: DBDep, user_data: UserEnter, response: Response):
    try:
        access_token = await AuthService(db).login_user(user_data)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
    response.set_cookie("access_token", access_token)
    return "Вы успешно вошли в систему"

@router.get("/me", summary="Получить информацию обо мне")
async def get_me(db: DBDep, request: Request):
    try:
        token = request.cookies.get("access_token", None)
        if not token:
            raise TokenExpiredHTTPException
        decode_token = AuthService(db).decode_token(token)
        user_id = decode_token.get("user_id")
        await AuthService(db).get_me(user_id)
        return await AuthService(db).get_me(user_id)

    except UserNotFoundException:
        raise UserNotFoundHTTPException
    except UserNotEnoughRightsException:
        raise UserNotEnoughRightsHTTPException
    except ExpiredSignatureError:
        raise TokenExpiredHTTPException

@router.get("/my_tasks", summary="Посмотреть мои задачи")
async def get_my_tasks(db: DBDep, request: Request):
    try:
        token = request.cookies.get("access_token", None)
        if not token:
            raise TokenExpiredHTTPException
        decode_token = AuthService(db).decode_token(token)
        user_id = decode_token.get("user_id")
        return await TaskService(db).get_user_tasks(user_id)
    except TaskNotFoundException:
        raise TaskNotFoundHTTPException


@router.post("/logout", summary="Выйти из системы")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return "Вы успешно вышли из системы"