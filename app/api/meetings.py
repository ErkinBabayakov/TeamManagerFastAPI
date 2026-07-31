from fastapi import APIRouter, Request, Response

from app.dependencies import DBDep, ManagerAdminDep
from app.exceptions import UsersInMeetingsNotFoundException, UsersInMeetingsNotFoundHTTPException, \
    TeamNotFoundException, TeamNotFoundHTTPException, UserNotEnoughRightsHTTPException, UserNotFoundException, \
    UserNotFoundHTTPException, TokenExpiredException, TokenExpiredHTTPException, EmailNotRegisteredException, \
    EmailNotRegisteredHTTPException, IncorrectPasswordException, IncorrectPasswordHTTPException, \
    UserNotManagerOrAdminException, UserNotManagerOrAdminHTTPException, MeetingNotFoundException, \
    MeetingNotFoundHTTPException, DataBaseException, DataBaseHTTPException
from app.schemas.meetings import MeetingRequestAdd
from app.schemas.users import UserEnter
from app.services.auth import AuthService
from app.services.meetings import MeetingsService

router = APIRouter(prefix="/meetings", tags=["Эндпоинты для встреч"])

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


@router.post("/teams/{team_id}/meetings", summary="Создать встречу")
async def create_meeting(db: DBDep, team_id: int, request: Request, meeting_data: MeetingRequestAdd, token: ManagerAdminDep):
    try:
        if token:
            current_user_access_token = request.cookies.get("access_token")
            decode_access_token = AuthService(db).decode_token(current_user_access_token)
            organizer_id = decode_access_token.get("user_id", None)
            return await MeetingsService(db).create_meeting(team_id, organizer_id, meeting_data)
        else:
            raise UserNotEnoughRightsHTTPException
    except TeamNotFoundException:
        raise TeamNotFoundHTTPException
    except UsersInMeetingsNotFoundException:
        raise UsersInMeetingsNotFoundHTTPException
    except UserNotFoundException:
        raise UserNotFoundHTTPException

@router.get("/{meeting_id}", summary="Посмотреть информацию о встрече")
async def get_meetings(db: DBDep, token: ManagerAdminDep, meeting_id: int):
    try:
        if token:
            return await MeetingsService(db).get_meetings(meeting_id)
        else:
            raise UserNotEnoughRightsHTTPException
    except MeetingNotFoundException:
        raise MeetingNotFoundHTTPException

@router.delete("/meetings/{meeting_id}", summary="Отменить встречу")
async def cancel_meeting(db: DBDep, meeting_id: int, token: ManagerAdminDep):
    try:
        if token:
            await MeetingsService(db).cancel_meeting(meeting_id)
            return "Встреча успешно отменена"
        else:
            raise UserNotEnoughRightsHTTPException
    except MeetingNotFoundException:
        raise MeetingNotFoundHTTPException
    except DataBaseException:
        raise DataBaseHTTPException



