import logging

from asyncpg import UniqueViolationError
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError, NoResultFound

from app.exceptions import ObjectAlreadyExistsException, TaskNotFoundException, TaskStatusException
from app.models import TaskOrm
from app.models.tasks import TaskStatus
from app.repositories.base import BaseRepository
from app.repositories.mappers.mappers import TaskDataMapper



class TaskRepository(BaseRepository):
    model = TaskOrm
    mapper = TaskDataMapper

    async def add_task(self, data: BaseModel, exclude_unset: bool = False, exclude_none: bool = False):
        try:
            add_data_stmt = insert(self.model).values(**data.model_dump(exclude_unset=exclude_unset, exclude_none=exclude_none)).returning(self.model)
            result = await self.session.execute(add_data_stmt)
            model = result.scalars().one()
            return self.mapper.map_to_domain_entity(model)
        except IntegrityError as ex:
            logging.exception(f"Не удалось добавить данные в БД, входные данные={data}")
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsException from ex
            else:
                logging.exception("Неизвестная ошибка")
                raise ex

    async def check_task_exists(self, task_id: int) -> bool:
        try:
            query = select(self.model).filter_by(id=task_id)
            result = await self.session.execute(query)
            model = result.scalars().one()
            if model:
                return True
            return False
        except NoResultFound as ex:
            raise TaskNotFoundException from ex

    async def check_task_status(self, task_id: int) -> bool:
        try:
            query = select(self.model).where(self.model.id == task_id, self.model.status == TaskStatus.done)
            result = await self.session.execute(query)
            model = result.scalars().first()
            if model:
                return True
            return False
        except NoResultFound as ex:
            raise TaskStatusException from ex

    async def get_title_task(self, assignee_id: int):
        try:
            query = select(self.model.title).filter_by(assignee_id=assignee_id)
            result = await self.session.execute(query)
            return result.scalars().all()
        except NoResultFound as ex:
            raise TaskStatusException from ex

    async def get_tasks(self, team_ids: list, from_date: datetime, to_date: datetime):
        try:
            query = select(self.model).filter(self.model.team_id.in_(team_ids),
                                              self.model.due_date >= from_date,
                                              self.model.due_date <= to_date)
            result = await self.session.execute(query)
            model = result.scalars().all()
            return model
        except NoResultFound as ex:
            raise TaskNotFoundException from ex


