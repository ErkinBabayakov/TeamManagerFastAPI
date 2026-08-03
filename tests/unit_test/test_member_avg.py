from app.dependencies import DBDep
from app.services.tasks import TaskService



async def test_member_avg(db: DBDep):
    avg = await TaskService(db).get_my_evaluations(assignee_id=1)
    assert avg
    result = []
    for a in avg[0]:
        score = a.get("score", None)
        if score:
            result.append(int(score))
        continue

    text = avg[1]
    num_str = text.split("=")[1].strip()
    value = float(num_str)
    assert sum(result) / len(result) == value


