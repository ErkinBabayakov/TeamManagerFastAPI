from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound, IntegrityError

from app.exceptions import TeamOrUserNotFoundException, MemberRoleUpdateException, ObjectNotFoundException
from app.models import TeamMemberOrm
from app.repositories.base import BaseRepository
from app.repositories.mappers.mappers import TeamMemberDataMapper



class TeamMemberRepository(BaseRepository):
    model = TeamMemberOrm
    mapper = TeamMemberDataMapper

    async def check_user_exists_team(self, team_id: int, user_id: int):
        try:
            query = select(self.model).filter(self.model.team_id == team_id,
                                              self.model.user_id == user_id)
            result = await self.session.execute(query)
            model = result.scalars().one_or_none()
            if model is None:
                return None
            return self.mapper.map_to_domain_entity(model)

        except NoResultFound as ex:
            raise TeamOrUserNotFoundException from ex


    async def get_list_members(self, team_id: int):
        try:
            query = select(self.model).filter(self.model.team_id == team_id)
            result = await self.session.execute(query)
            model = result.scalars().all()
            return model
        except NoResultFound as ex:
            raise TeamOrUserNotFoundException from ex


    async def update_member_role(self, team_id: int, user_id: int, role: str):
        try:
            update_data_stmt = update(self.model).where(self.model.team_id == team_id, self.model.user_id == user_id).values(role=role)
            await self.session.execute(update_data_stmt)
        except IntegrityError:
            raise MemberRoleUpdateException


    async def get_team_ids(self, current_user_id: int):
        try:
            query = select(self.model.team_id).filter(self.model.user_id == current_user_id)
            result = await self.session.execute(query)
            model = [tm.team_id for tm in result.all()]
            return model
        except NoResultFound as ex:
            raise ObjectNotFoundException from ex



