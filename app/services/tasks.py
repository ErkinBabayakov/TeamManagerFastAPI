from sqlalchemy.exc import IntegrityError, NoResultFound
from app.exceptions import TaskCreateException, TaskCreateHTTPException, TeamNotFoundException, ObjectNotFoundException, \
    TaskOrTeamNotFoundException, TeamTaskEmptyException, TaskNotFoundException
from app.schemas.tasks import TaskRequestAdd, TaskAdd, TaskPATCH, TaskUpdate
from app.services.base import BaseService


class TaskService(BaseService):

    async def create_task(self, team_id: int, creator_id:int , task_data: TaskRequestAdd):
        new_task_data = TaskAdd(
            team_id = team_id,
            creator_id = creator_id,
            title= task_data.title,
            description= task_data.description,
            assignee_id=task_data.assignee_id,
            due_date=task_data.due_date,
        )
        try:
            await self.db.tasks.add_task(new_task_data, exclude_none=True, exclude_unset=True)
            await self.db.commit()
        except TaskCreateException as ex:
            raise TaskCreateHTTPException from ex
        except IntegrityError as ex:
            raise TeamNotFoundException from ex

    async def get_task(self, team_id:int, task_id:int):
        try:
            task = await self.db.tasks.get_one(id=task_id, team_id=team_id)
            await self.db.commit()
            return task
        except ObjectNotFoundException:
            raise TaskOrTeamNotFoundException

    async def get_team_tasks(self, team_id:int):
        try:
            tasks = await self.db.tasks.get_all(team_id=team_id)
            if tasks:
                await self.db.commit()
                return tasks
            else:
                raise TeamTaskEmptyException
        except ObjectNotFoundException:
            raise TeamNotFoundException

    async def update_task(self, team_id:int, task_id:int, task_data: TaskPATCH):
        try:
            task_exists = await self.db.tasks.check_task_exists(task_id=task_id)
            team_exists = await self.db.teams.check_team_exists(team_id=team_id)
            if task_exists and team_exists:
                task_data_update = TaskUpdate(
                    title= task_data.title,
                    description= task_data.description,
                    assignee_id=task_data.assignee_id,
                    due_date=task_data.due_date,
                    status = task_data.status,
                )
                await self.db.tasks.edit(task_data_update,  exclude_unset=True, exclude_none=True,  id=task_id, team_id=team_id)
                await self.db.commit()
            else:
                raise TaskOrTeamNotFoundException
        except ObjectNotFoundException:
            raise TaskOrTeamNotFoundException

    async def delete_task(self, team_id:int, task_id:int):
        try:
            task_exists = await self.db.tasks.check_task_exists(task_id=task_id)
            team_exists = await self.db.teams.check_team_exists(team_id=team_id)
            if task_exists and team_exists:
                await self.db.tasks.delete(id=task_id, team_id=team_id)
                await self.db.commit()
            else:
                raise TaskOrTeamNotFoundException
        except ObjectNotFoundException as ex:
            raise TaskOrTeamNotFoundException from ex

    async def get_user_tasks(self, assignee_id: int):
        try:
            tasks = await self.db.tasks.get_all(assignee_id=assignee_id)
            if tasks:
                await self.db.commit()
                return [{"Заголовок задачи": task.title, "Описание": task.description} for task in tasks]
            else:
                raise TaskNotFoundException
        except ObjectNotFoundException:
            raise TaskNotFoundException




