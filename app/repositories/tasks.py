import logging

from asyncpg import UniqueViolationError
from pydantic import BaseModel
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError, NoResultFound

from app.exceptions import ObjectAlreadyExistsException, ObjectNotFoundException
from app.models import TaskOrm
from app.repositories.base import BaseRepository
from app.repositories.mappers.mappers import TaskDataMapper
from app.schemas.tasks import TaskPATCH


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
            result = result.scalars().one()
            if result:
                return True
            return False
        except NoResultFound as ex:
            raise ObjectNotFoundException from ex
