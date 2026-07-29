from app.exceptions import TeamNotFoundException, InvalidInviteCodeException, UserAlreadyExistsException, \
    ObjectAlreadyExistsException, UserInviteAlreadyExistsException, ObjectNotFoundException, TeamEmptyException, \
    TeamManagerException, UserNotFoundException, TeamOrUserNotFoundException, MemberRoleUpdateException
from app.schemas.teammembers import JoinTeam, TeamMemberAdd, TeamMemberPATCH, TeamMemberPATCHRole
from app.services.base import BaseService


class TeamMembersService(BaseService):
    async def join_team(self, team_id: int, user_id: int, join_data: JoinTeam):
        team = await self.db.teams.get_team(team_id)
        if not team:
            raise TeamNotFoundException
        if team.invite_code != join_data.invite_code:
            raise InvalidInviteCodeException
        existing = await self.db.team_members.check_user_exists_team(team_id, user_id)
        if existing:
            raise UserInviteAlreadyExistsException
        try:
            new_user = TeamMemberAdd(
                team_id=team_id,
                user_id=user_id,
                first_name=join_data.first_name,
                last_name=join_data.last_name,
                role=join_data.role,
            )
            await self.db.team_members.add(new_user)
            await self.db.commit()
        except ObjectAlreadyExistsException as ex:
            raise UserAlreadyExistsException from ex

    async def get_list_members(self, team_id: int):
        try:
            list_members = await self.db.team_members.get_list_members(team_id=team_id)
            if not list_members:
                raise TeamEmptyException
            return list_members
        except ObjectNotFoundException as ex:
            raise TeamNotFoundException from ex

    async def update_member_role(self, team_id: int, user_id: int, update_data: TeamMemberPATCHRole):
        try:
            team_exists = await self.db.teams.check_team_exists(team_id=team_id)
            user_exists = await self.db.users.check_user_exists(user_id=user_id)
            if team_exists and user_exists:
                await self.db.team_members.update_member_role(team_id=team_id, user_id=user_id, role=update_data.role)
                await self.db.commit()
            else:
                raise TeamOrUserNotFoundException
        except MemberRoleUpdateException as ex:
            raise TeamOrUserNotFoundException from ex

    async def delete_member(self, team_id: int, user_id: int):
        try:
            team_exists = await self.db.teams.check_team_exists(team_id=team_id)
            user_exists = await self.db.users.check_user_exists(user_id=user_id)
            if team_exists and user_exists:
                await self.db.team_members.delete(team_id=team_id, user_id=user_id)
                await self.db.commit()
            else:
                raise TeamOrUserNotFoundException
        except ObjectNotFoundException as ex:
            raise TeamOrUserNotFoundException from ex
