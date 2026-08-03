from datetime import datetime, timezone
from app.exceptions import TeamNotFoundException, InvalidInviteCodeException, UserAlreadyExistsException, \
    ObjectAlreadyExistsException, UserInviteAlreadyExistsException, ObjectNotFoundException, TeamEmptyException, \
    TeamOrUserNotFoundException, MemberRoleUpdateException
from app.schemas.calendar import CalendarEvent, CalendarEventValidateDate
from app.schemas.teammembers import JoinTeam, TeamMemberAdd, TeamMemberPATCHRole
from app.services.base import BaseService


class TeamMembersService(BaseService):
    """Сервисный слой для участников команды"""

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

    async def get_team_ids(self, current_user_id, from_date: datetime, to_date: datetime):
        try:
            # Команды пользователя
            team_ids = await self.db.team_members.get_team_ids(current_user_id)
            if not team_ids:
                return []

            validate_data = CalendarEventValidateDate(
                start=from_date,
                end=to_date,
            )
            # Задачи: due_date в диапазане
            tasks = await self.db.tasks.get_tasks(team_ids, validate_data.start, validate_data.end)

            # Встречи, где пользователь участник
            meetings = await self.db.meetings.get_meetings(current_user_id, validate_data.start, validate_data.end)
            events = []
            for task in tasks:
                events.append(CalendarEvent(
                    id=task.id, title=task.title, start=task.start,
                    end=task.end, type="task", status=task.status
                ))
            for meeting in meetings:
                events.append(CalendarEvent(
                    id=meeting.id, title=meeting.title, start=meeting.starts_at,
                    end=meeting.ends_at, type="meeting", status=None
                ))
            return events

        except ValueError as ex:
            raise ValueError from ex

    def to_naive_utc(self, dt: datetime) -> datetime:
        if dt.tzinfo is not None:
            return dt.astimezone(timezone.utc).replace(tzinfo=None)
        return dt



