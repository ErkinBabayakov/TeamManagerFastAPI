import pytest
from httpx import AsyncClient
from enum import Enum
from typing import Optional

from app.services.auth import AuthService


class UserRole(str, Enum):
    member = "member"
    manager = "manager"
    admin = "admin"


@pytest.mark.parametrize(
    "email, password, first_name, last_name, role, status_code",
    [
        ("kot1@pes.com", "1234", "kot1", "pes1",  "admin", 200),
        ("kot2@pes.com", "1234", "kot2", "pes2",  "member",  200),
        ("kot3@pes.com", "1234", "kot2", "pes2",  "manager",  200),
        ("kot2@pes.com", "1234", "kot1", "pes1",  "member",  409),
        ("abcde", "1234", "abc", "cde",  "member", 422),
        ("abcde@acbde", "1234", "abc", "cde", "admin", 422),
    ],
)
async def test_admin_flow(
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    role: Optional[UserRole],
    status_code: int,
    ac: AsyncClient,
    register_user,
    authenticated_ac
):
    # /register
    resp_register = await ac.post(
        "/admin/register",
        json={
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "role": role,
        },
    )
    assert resp_register.status_code == status_code
    if status_code != 200:
        return

    resp_register2 = await authenticated_ac.patch(
        "/admin/register",
        json={
            "password": password,
            "first_name": first_name,
            "last_name": last_name,

        },
    )
    assert resp_register2.status_code == 404

    # /login
    resp_login = await ac.post(
    "/admin/login", json={"email": email, "password": password}
)
    if role == UserRole.member or role == UserRole.manager:
        pytest.skip("Данному пользователю доступ запрещен")
    assert resp_login.status_code == 200
    assert ac.cookies["access_token"]
    assert resp_register.status_code == status_code
    assert "access_token" in resp_login.cookies

    #/user_info
    user_data = resp_login.cookies["access_token"]
    user_id = AuthService().decode_token(user_data).get("user_id")
    resp_me = await ac.get(f"/admin/{user_id}/user_info")
    assert resp_me.status_code == status_code
    user = resp_me.json()
    assert "id" in user
    assert user["email"] == email
    assert "password" not in user
    assert "hashed_password"  not in user


    # /logout
    resp_logout = await ac.post("/admin/logout")
    assert resp_register.status_code == status_code
    assert "access_token " not in resp_logout.cookies


