from fastapi import Depends, HTTPException, Request
from typing import Annotated
from jwt.exceptions import ExpiredSignatureError

from app.database import async_session_maker
from app.exceptions import TokenExpiredHTTPException
from app.services.auth import AuthService
from app.utils.db_manager import DBManager


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401, detail="Вы не предоставилил токен доступа")
    return token

def check_user_is_admin(request: Request) -> bool:
    try:
        token = request.cookies.get("access_token", None)
        if not token:
            raise HTTPException(status_code=401, detail="Вы не предоставилил токен доступа")
        data = AuthService().decode_token(token)
        if data.get("role") != "admin":
            return False
        return True
    except ExpiredSignatureError:
        raise TokenExpiredHTTPException

UserTokenDep = Annotated[bool, Depends(check_user_is_admin)]



def check_user_is_manager_or_admin(request: Request) -> bool:
    try:
        token = request.cookies.get("access_token", None)
        if not token:
            raise HTTPException(status_code=401, detail="Вы не предоставилил токен доступа")
        data = AuthService().decode_token(token)
        if data.get("role") == "manager" or data.get("role") != "admin":
            return True
        return False
    except ExpiredSignatureError:
        raise TokenExpiredHTTPException

ManagerAdminDep = Annotated[bool, Depends(check_user_is_manager_or_admin)]


def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().decode_token(token)
    return data.get("user_id", None)

UserIdDep = Annotated[int, get_current_user_id]



async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
