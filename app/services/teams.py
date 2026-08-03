import secrets
from app.exceptions import ObjectAlreadyExistsException, TeamAlreadyExistsException, ObjectNotFoundException, TeamNotExistException
from app.schemas.teams import TeamRequestAdd, TeamAdd
from app.services.base import BaseService


class TeamService(BaseService):
    """Сервисный слой для команды"""

    async def create_team(self, team_data: TeamRequestAdd, creator_id: int):
        invite_code = secrets.token_urlsafe(12)
        _team_data = TeamAdd(
            name=team_data.name,
            invite_code=invite_code,
            creator_id=creator_id,
        )
        try:
            await self.db.teams.add(_team_data)
            await self.db.commit()
            return f"Команда успешно создана, пригласить участника в команду можно по invite_code: {invite_code}"
        except ObjectAlreadyExistsException as ex:
            raise TeamAlreadyExistsException from ex


    async def get_list_teams(self):
        try:
            teams = await self.db.teams.get_all()
            if teams:
                return teams
            else:
                raise TeamNotExistException
        except ObjectNotFoundException as ex:
            raise TeamNotExistException from ex






