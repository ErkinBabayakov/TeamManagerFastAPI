from fastapi import APIRouter, Request, Response
from app.dependencies import DBDep, ManagerAdminDep
from app.exceptions import UserNotEnoughRightsHTTPException, TaskCreateException, TaskCreateHTTPException, \
    TeamNotFoundException, TeamNotFoundHTTPException, \
    TaskOrTeamNotFoundException, TaskOrTeamNotFoundHTTPException, TeamTaskEmptyException, TeamTaskEmptyHTTPException, \
    TokenExpiredException, TokenExpiredHTTPException, EmailNotRegisteredException, EmailNotRegisteredHTTPException, \
    IncorrectPasswordException, IncorrectPasswordHTTPException, UserNotManagerOrAdminException, \
    UserNotManagerOrAdminHTTPException, TeamOrUserNotFoundException, TeamOrUserNotFoundHTTPException, \
    TaskNotFoundException, TaskNotFoundHTTPException, TaskStatusException, TaskStatusHTTPException, EvalCreateException, \
    EvalCreateHTTPException
from app.schemas.evaluations import EvaluationRequestAdd
from app.schemas.tasks import TaskRequestAdd, TaskPATCH
from app.schemas.users import UserEnter
from app.services.auth import AuthService
from app.services.tasks import TaskService

router = APIRouter(prefix="/manager_tasks", tags=["Эндпоинты менеджера для управления задачами"])

@router.post("/login", summary="Войти в систему", description="Введите email и пароль")
async def login_user(db: DBDep, user_data: UserEnter, response: Response):
    try:
        access_token = await AuthService(db).login_manager(user_data)
    except TokenExpiredException:
        raise TokenExpiredHTTPException
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException

    except UserNotManagerOrAdminException:
        raise UserNotManagerOrAdminHTTPException
    response.set_cookie("access_token", access_token)
    return "Вы успешно вошли в систему"


@router.post("/create_task", summary="Создать задачу")
async def create_task(db: DBDep, team_id: int, task_data: TaskRequestAdd, token: ManagerAdminDep, request: Request):
    try:
        if token:
            creator_member_token = request.cookies.get("access_token")
            decode_member_token = AuthService(db).decode_token(creator_member_token)
            creator_id = decode_member_token.get("user_id", None)
            await TaskService(db).create_task(team_id, creator_id, task_data)
            return "Вы успешно создали задачу"
        else:
            raise UserNotEnoughRightsHTTPException
    except TaskCreateException:
        raise TaskCreateHTTPException
    except TeamNotFoundException:
        raise TeamNotFoundHTTPException

@router.get("/{task_id}", summary="Получить задачу по task_id")
async def get_task(db: DBDep, team_id: int, task_id: int, token: ManagerAdminDep):
    try:
        if token:
            return await TaskService(db).get_task(team_id, task_id)
        else:
            raise UserNotEnoughRightsHTTPException
    except TaskOrTeamNotFoundException:
        raise TaskOrTeamNotFoundHTTPException

@router.get("/{team_id}/tasks", summary="Получить список задач для команды")
async def get_team_tasks(db: DBDep, team_id: int, token: ManagerAdminDep):
    try:
        if token:
            return await TaskService(db).get_team_tasks(team_id)
        else:
            raise UserNotEnoughRightsHTTPException
    except TeamNotFoundException:
        raise TeamNotFoundHTTPException
    except TeamTaskEmptyException:
        raise TeamTaskEmptyHTTPException

@router.post("/tasks/{task_id}/evaluation", summary="Поставить оценку к выполненной задаче")
async def evaluate_task(db: DBDep, task_id: int, eval_data: EvaluationRequestAdd, token: ManagerAdminDep, request: Request):
    try:
        if token:
            evaluator_token = request.cookies.get("access_token")
            decode_evaluator_token = AuthService(db).decode_token(evaluator_token)
            evaluator_id = decode_evaluator_token.get("user_id", None)
            await TaskService(db).evaluate_task(task_id, eval_data, evaluator_id)
            return "Оценка успешно проставлена"
        else:
            raise UserNotEnoughRightsHTTPException
    except TaskNotFoundException:
        raise TaskNotFoundHTTPException
    except TaskStatusException:
        raise TaskStatusHTTPException
    except EvalCreateException:
        raise EvalCreateHTTPException


@router.patch("/update_task/{task_id}", summary="Обновить задачу")
async def update_task(db: DBDep, team_id: int, task_id: int, update_data: TaskPATCH, token: ManagerAdminDep):
    try:
        if token:
            await TaskService(db).update_task(team_id, task_id, update_data)
            return "Задача успешно обновлена"
        else:
            raise UserNotEnoughRightsHTTPException
    except TaskOrTeamNotFoundException:
        raise TaskOrTeamNotFoundHTTPException

@router.delete("/delete_task/{task_id}", summary="Удалить задачу")
async def delete_task(db: DBDep, team_id: int, task_id: int, token: ManagerAdminDep):
    try:
        if token:
            await TaskService(db).delete_task(team_id, task_id)
            return "Задача успешно удалена"
        else:
            raise UserNotEnoughRightsHTTPException
    except TaskOrTeamNotFoundException:
        raise TaskOrTeamNotFoundHTTPException




