import logging

from asyncpg import UniqueViolationError
from pydantic import BaseModel
from sqlalchemy import insert, select, func
from sqlalchemy.exc import IntegrityError

from app.exceptions import ObjectAlreadyExistsException, ObjectNotFoundException
from app.models import EvaluationOrm, TaskOrm
from app.repositories.base import BaseRepository

from app.repositories.mappers.mappers import EvaluationDataMapper



class EvaluationRepository(BaseRepository):
    model = EvaluationOrm
    mapper = EvaluationDataMapper

    async def add_evaluation(self, data: BaseModel, exclude_unset: bool = False, exclude_none: bool = False):
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


    async def get_my_evaluations(self, assignee_id: int):
       try:
            query = (
                select(TaskOrm.title, EvaluationOrm.score, EvaluationOrm.comment)
                .outerjoin(TaskOrm.evaluation)
                .where(TaskOrm.assignee_id == assignee_id)
            )
            result = await self.session.execute(query)
            model = result.mappings().all()

            avg_query = select(func.avg(EvaluationOrm.score)).join(TaskOrm.evaluation).where(TaskOrm.assignee_id == assignee_id)
            avg_result = await self.session.execute(avg_query)
            avg = avg_result.scalars().one()
            return {"eval_data": model, "avg_eval": avg}
       except TypeError as ex:
           raise ObjectNotFoundException from ex


