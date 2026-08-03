from fastapi import APIRouter, Query, Request, Response
from datetime import datetime
from jwt.exceptions import ExpiredSignatureError
from app.dependencies import DBDep
from app.exceptions import EmailNotRegisteredException, EmailNotRegisteredHTTPException, IncorrectPasswordException, \
    IncorrectPasswordHTTPException, TokenExpiredHTTPException, UserNotFoundException, UserNotFoundHTTPException, \
    UserNotEnoughRightsException, UserNotEnoughRightsHTTPException
from app.schemas.calendar import CalendarEvent
from app.schemas.users import UserEnter
from app.services.auth import AuthService
from app.services.teammembers import TeamMembersService

router = APIRouter(prefix="/calendar", tags=["Календарь для встреч"])


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

@router.get("/", response_model=list[CalendarEvent], summary="Посмотреть события в календаре, даты ставятся с часовым поясом (tz)")
async def get_calendar(db: DBDep, request: Request, from_date: datetime = Query(...), to_date: datetime = Query(...)):
    current_user_token = request.cookies.get("access_token")
    decode_token = AuthService(db).decode_token(current_user_token)
    current_user_id = decode_token.get("user_id", None)

    start_naive_utc = TeamMembersService(db).to_naive_utc(from_date)
    end_naive_utc = TeamMembersService(db).to_naive_utc(to_date)
    return await TeamMembersService(db).get_team_ids(current_user_id, start_naive_utc, end_naive_utc)