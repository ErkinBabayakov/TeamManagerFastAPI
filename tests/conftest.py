# ruff: noqa: E402
import pytest

from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator
from app.dependencies import get_db
from app.main import app
from app.config import settings
from app.database import Base, engine_null_pool, async_session_maker_null_pool
from app.models import *  # noqa
from app.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db

# Перезаписывам зависимость с session_factory=async_session_maker на async_session_maker_null_pool (
app.dependency_overrides[get_db] = get_db_null_pool

@pytest.fixture(scope="function")
async def db() -> AsyncGenerator[DBManager, None]:
    async for db in get_db_null_pool():
        yield db


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="session")
async def register_user(ac, setup_database):
    await ac.post(
        "/admin/register",
        json={
            "email": "kot@pes.com",
            "password": "1234",
            "first_name": "kot",
            "last_name": "pes",
            "role": "admin",
        },
    )

# @pytest.fixture(scope="session")
# async def register_member(ac, setup_database):
#     await ac.post(
#         "/admin/register",
#         json={"email": "prosto@member.com", "password": "1234",
#               "first_name": "prosto", "last_name": "member",
#               "role": "member",}
#     )

@pytest.fixture(scope="session")
async def register_manager(ac, setup_database):
    await ac.post(
        "/admin/register",
        json={
            "email": "ManagerSuper@pes.com",
            "password": "1234",
            "first_name": "Manager",
            "last_name": "SuperManager",
            "role": "manager",
        },
    )

@pytest.fixture(scope="session")
async def authenticated_ac(ac, register_user):
    await ac.post("/admin/login",
        json={"email": "kot@pes.com", "password": "1234",})
    assert ac.cookies.get("access_token")
    yield ac

# @pytest.fixture(scope="session")
# async def authenticated_member(ac, register_member):
#     await ac.post("/member/login", json={"email": "prosto@member.com", "password": "1234"})
#     assert ac.cookies.get("access_token")
#     yield ac


@pytest.fixture(scope="session")
async def register_team(ac, setup_database):
    response = await ac.post("/manager/register/team",
                  json={"name": "Super Dogs"}
    )
    data = response.json()
    print(data)
    if data:
        import re
        match = re.search(r"invite_code: (\S+)", data)
        invite_code = match.group(1).strip() if match else None
        print(invite_code)
        return {"id": 1,
            "invite_code": invite_code,
        }

@pytest.fixture(scope="session")
async def manager_login(ac, register_manager):
    await ac.post("/manager/login", json={"email": "ManagerSuper@pes.com", "password": "1234"})
    assert ac.cookies.get("access_token")
    yield ac


@pytest.fixture(scope="session")
async def check_register_team(ac, setup_database):
    await ac.post("/manager/register/team",
                  json={"name": "Super Dogs"})



@pytest.fixture(scope="session")
async def register_task(manager_login, setup_database, register_team):
    resp_task = await manager_login.post("/manager_tasks/create_task",  params={"team_id": register_team.get("id")}, json={
        "title": "Test Task",
        "description": "This is a test task",
        "assignee_id": 1
    })
    print(resp_task)
    return resp_task