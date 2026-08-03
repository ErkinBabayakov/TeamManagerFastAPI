from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from app.exceptions import TeamNotFoundException
from app.models import TeamOrm
from app.repositories.base import BaseRepository
from app.repositories.mappers.mappers import TeamDataMapper
from app.schemas.teams import Team


class TeamRepository(BaseRepository):
    model = TeamOrm
    mapper = TeamDataMapper

    async def get_team(self, team_id: int):
        try:
            query = select(self.model).filter_by(id=team_id)
            result = await self.session.execute(query)
            model = result.scalars().first()
            return Team.model_validate(model)
        except NoResultFound as ex:
            raise TeamNotFoundException from ex

    async def check_team_exists(self, team_id: int):
        try:
            query = select(self.model).filter_by(id=team_id)
            result = await self.session.execute(query)
            model = result.scalars().first()
            if model:
                return True
            return False
        except NoResultFound as ex:
            raise TeamNotFoundException from ex