from fastapi import APIRouter, Response, Request, Body
from jwt.exceptions import ExpiredSignatureError
from app.dependencies import DBDep, ManagerAdminDep
from app.exceptions import EmailNotRegisteredException, EmailNotRegisteredHTTPException, IncorrectPasswordException, \
    IncorrectPasswordHTTPException, TokenExpiredHTTPException, UserNotFoundException, UserNotFoundHTTPException, \
    UserNotEnoughRightsException, UserNotEnoughRightsHTTPException, TokenExpiredException, \
    UserNotManagerOrAdminException, UserNotManagerOrAdminHTTPException, TeamOrUserNotFoundException, \
    TeamOrUserNotFoundHTTPException, InvalidInviteCodeException, InvalidInviteCodeHTTPException, \
    UserAlreadyExistsException, UserInviteAlreadyExistsHTTPException, UserInviteAlreadyExistsException, \
    TeamAlreadyExistsException, TeamAlreadyExistsHTTPException, TeamNotFoundHTTPException, TeamNotFoundException, \
    TeamEmptyException, TeamEmptyHTTPException, TeamNotExistException, TeamNotExistHTTPException, \
    MemberRoleUpdateException, MemberRoleUpdateHTTPException
from app.schemas.teammembers import JoinTeam, TeamMemberPATCH, TeamMemberPATCHRole
from app.schemas.teams import TeamRequestAdd
from app.schemas.users import UserEnter
from app.services.auth import AuthService
from app.services.teammembers import TeamMembersService
from app.services.teams import TeamService

router = APIRouter(prefix="/manager", tags=["Эндпоинты менеджера для создания и управления командами"])


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

@router.get("/me", summary="Получить информацию обо мне")
async def get_me(db: DBDep, request: Request):
    try:
        token = request.cookies.get("access_token", None)
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


@router.post("/register/team", summary="Создать команду")
async def register_team(db:DBDep, request: Request, token: ManagerAdminDep, team_data: TeamRequestAdd):
    try:
        if token:
            token_user = request.cookies.get("access_token", None)
            decode_token = AuthService(db).decode_token(token_user)
            creator_id = decode_token.get("user_id", None)
            return await TeamService(db).create_team(team_data, creator_id)
        else:
            raise UserNotEnoughRightsHTTPException
    except TeamAlreadyExistsException:
        raise TeamAlreadyExistsHTTPException

@router.post("/{team_id}/join", summary="Добавить в команду пользователя")
async def join_team(db: DBDep, team_id: int, user_id: int, join_data: JoinTeam, token: ManagerAdminDep):
    try:
        if token:
            await TeamMembersService(db).join_team(team_id, user_id, join_data)
            return "Вы успешно добавили пользователя в команду"
        else:
            raise UserNotEnoughRightsHTTPException
    except TeamOrUserNotFoundException:
        raise TeamOrUserNotFoundHTTPException
    except InvalidInviteCodeException:
        raise InvalidInviteCodeHTTPException
    except UserInviteAlreadyExistsException:
        raise UserInviteAlreadyExistsHTTPException


@router.get("/members", summary="Показать список участников в команде")
async def get_list_members(db: DBDep, team_id: int, token: ManagerAdminDep):
    try:
        if token:
            return await TeamMembersService(db).get_list_members(team_id)
        else:
            raise UserNotEnoughRightsHTTPException
    except TeamNotFoundException:
        raise TeamNotFoundHTTPException
    except TeamEmptyException:
        raise TeamEmptyHTTPException

@router.get("/teams", summary="Получить список команд")
async def get_list_teams(db:DBDep, token: ManagerAdminDep):
    try:
        if token:
            return await TeamService(db).get_list_teams()
        else:
            raise UserNotEnoughRightsHTTPException
    except TeamNotExistException:
        raise TeamNotExistHTTPException

@router.patch("/{user_id}/update_member", summary="Обновить роль пользователя в команде")
async def update_member_role(db: DBDep, team_id: int, user_id: int, update_data: TeamMemberPATCHRole, token: ManagerAdminDep):
    try:
        if token:
            await TeamMembersService(db).update_member_role(team_id, user_id, update_data)
            return "Обновление роли произошло успешно"
        else:
            raise UserNotEnoughRightsHTTPException
    except TeamOrUserNotFoundException:
        raise TeamOrUserNotFoundHTTPException
    except MemberRoleUpdateException:
        raise MemberRoleUpdateHTTPException

@router.delete("/delete_member", summary="Исключить пользователя из команды")
async def delete_member(db: DBDep, team_id: int, user_id: int, token: ManagerAdminDep):
    try:
        if token:
            await TeamMembersService(db).delete_member(team_id, user_id)
            return "Пользователь исключен из команды"
        else:
            raise UserNotEnoughRightsHTTPException
    except TeamOrUserNotFoundException:
        raise TeamOrUserNotFoundHTTPException


@router.post("/logout", summary="Выйти из системы")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return "Вы успешно вышли из системы"