import pytest
from httpx import AsyncClient

@pytest.mark.parametrize(
    "team_id, title, description, assignee_id, status_code",
    [
        (1, "Первая задача", "Просто большушщая задача",  1, 200),
        (1, "Вторая задача", "Просто большушщая задача",  1, 200),
        (1, "Третья задача", "Просто большушщая задача",  "addwa", 422),
        (1, "Третья задача", 123,  "addwa", 422),
        (500, "Четвертая задача", "Просто большушщая задача", 1, 404)
    ]
)
async def test_add_task(team_id: int, title: str, description: str,  assignee_id: int, status_code: int, manager_login: AsyncClient):
    response_task = await manager_login.post("/manager_tasks/create_task", params={"team_id": team_id}, json={
        "title": title,
        "description": description,
        "assignee_id": assignee_id,
    })
    print(response_task.text)
    assert response_task.status_code == status_code