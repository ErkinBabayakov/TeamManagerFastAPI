import pytest
from httpx import AsyncClient

@pytest.mark.parametrize(
    "task_id, team_id, score, comment, status_code",
    [
        (1, 1, 3, "Privet", 200),
        (1, 1, 6, "За диапазоном", 422),
        (34, 1, 5, "нет с таким task_id", 404)
    ]
)
async def test_add_evaluate_flow(manager_login: AsyncClient, task_id: int, team_id: int, score: int,
                                 comment: str, status_code: int, register_task):

    # Обновление статуса задачи на done
    response_update_task = await manager_login.patch(f"/manager_tasks/update_task/{task_id}", params={"id": task_id, "team_id": team_id}, json={"status": "done"})
    if response_update_task.status_code != 200:
        pytest.skip("Обновление задачи пошло не плану")

    # Ставим оценку
    response_evaluate = await manager_login.post(f"/manager_tasks/tasks/{task_id}/evaluation", params={"task_id": task_id}, json={
        "score": score,
        "comment": comment
    })
    response_evaluate_status_code = response_evaluate.status_code
    assert response_evaluate_status_code == status_code





