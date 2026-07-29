from fastapi import APIRouter, Request, Response, Path
from jwt.exceptions import ExpiredSignatureError
from app.dependencies import DBDep
from app.exceptions import EmailNotRegisteredException, EmailNotRegisteredHTTPException, IncorrectPasswordException, \
    IncorrectPasswordHTTPException, TokenExpiredHTTPException, TaskNotFoundException, TaskNotFoundHTTPException
from app.schemas.comments import CommentRequestAdd
from app.schemas.users import UserEnter
from app.services.auth import AuthService
from app.services.comments import CommentService

router = APIRouter(tags=['Эндпоинт для добавления и чтения комментариев к задаче'])

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

@router.post("/tasks/{task_id}/comments", summary="Добавить комментарий к задаче")
async def add_comment(db: DBDep, comment_data: CommentRequestAdd, request: Request, task_id: int = Path(description="Укажите валидный task_id задачи")):
    try:
        access_token = request.cookies.get("access_token")
        user_decode_token = AuthService(db).decode_token(access_token)
        author_id = user_decode_token.get("user_id", None)
        await CommentService(db).add_comment(task_id, author_id, comment_data)
        return "Комментарий к указанной задаче добавлен"
    except ExpiredSignatureError:
        raise TokenExpiredHTTPException
    except TaskNotFoundException:
        raise TaskNotFoundHTTPException

@router.get("/comments", summary="Получить все комментарии к задаче")
async def get_comments(db: DBDep, task_id: int):
    try:
        return await CommentService(db).get_comments(task_id)
    except ExpiredSignatureError:
        raise TokenExpiredHTTPException
    except TaskNotFoundException:
        raise TaskNotFoundHTTPException