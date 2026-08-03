import pytest
from httpx import AsyncClient
from enum import Enum


class UserRole(str, Enum):
    member = "member"
    manager = "manager"
    admin = "admin"


team_data = {"first_name": "Alex", "last_name": "Gusev"}


async def test_team_member_add(manager_login: AsyncClient, register_team: dict, team_id=1, user_id=1,
                               first_name=team_data["first_name"], last_name=team_data["last_name"], role=UserRole.member):

    response_teammember = await manager_login.post(f"/manager/{team_id}/join", params={
        "team_id": team_id,
        "user_id": user_id,
    },
        json={
        "invite_code": register_team["invite_code"],
        "first_name": first_name,
        "last_name": last_name,
        "role": role
    })
    response_teammember_status_code = response_teammember.status_code
    assert response_teammember_status_code == 200


@pytest.mark.parametrize(
    "name, status_code",
    [("Crazy Dogs", 200),
     ("Crazy Dogs", 409),
     (123, 422)]
)

async def test_create_team(name: str, status_code: int,  manager_login: AsyncClient, check_register_team):

    #create team
    response_team = await manager_login.post("/manager/register/team", json={"name": name})
    response_team_status_code = response_team.status_code
    assert response_team_status_code == status_code



