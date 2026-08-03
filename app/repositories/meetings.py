from datetime import datetime
from typing import List
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload
from app.exceptions import TeamNotFoundException, UserNotFoundException, MeetingNotFoundException
from app.models import MeetingOrm, MeetingParticipantOrm, UserOrm, TeamMemberOrm
from app.repositories.base import BaseRepository
from app.repositories.mappers.mappers import MeetingDataMapper



class MeetingsRepository(BaseRepository):
    model = MeetingOrm
    mapper = MeetingDataMapper

    async def check_overlap(self, user_id: int, starts_at: datetime, ends_at: datetime, exclude_meeting_id: int = None):
        query = select(self.model).join(MeetingParticipantOrm).filter(
            MeetingParticipantOrm.user_id == user_id,
            self.model.starts_at < ends_at,
            self.model.ends_at > starts_at,
        )
        if exclude_meeting_id:
            query = query.filter(self.model.id != exclude_meeting_id)
        result = await self.session.execute(query)
        model = result.first()
        return model is not None

    async def check_participants(self, participants_ids: List[int]):
        query = select(UserOrm.id).filter(UserOrm.id.in_(participants_ids))
        result = await self.session.execute(query)
        model = result.all()
        participants = [m[0] for m in model]
        return participants

    async def check_member_participants(self, team_id: int, user_id: int):

        team_query = select(TeamMemberOrm.team_id).filter_by(team_id=team_id)
        if team_query is None:
            raise TeamNotFoundException
        user_query = select(UserOrm.id).filter_by(id=user_id)
        if user_query is None:
            raise UserNotFoundException

        query = select(TeamMemberOrm).filter(
            TeamMemberOrm.team_id == team_id,
            TeamMemberOrm.user_id == user_id,
        )
        result = await self.session.execute(query)
        model = result.mappings().first()
        return model



    async def get_meeting_data(self, all_participants: set):
        query = select(UserOrm.id, UserOrm.email,UserOrm.first_name, UserOrm.last_name, UserOrm.role).filter(UserOrm.id.in_(all_participants))
        result = await self.session.execute(query)
        model = result.mappings().all()
        return model


    async def get_meeting_with_participants(self, meeting_id: int) -> MeetingOrm:
        try:
            query = (
                select(self.model)
                .where(self.model.id == meeting_id)
                .options(
                    selectinload(self.model.participants).selectinload(MeetingParticipantOrm.user)
                )
            )
            result = await self.session.execute(query)
            model = result.scalar_one()
            return model
        except NoResultFound:
            raise MeetingNotFoundException


    async def get_meetings(self, current_user_id: int, from_date: datetime, to_date: datetime):
        try:
            query = select(self.model).join(MeetingParticipantOrm).filter(
                MeetingParticipantOrm.user_id == current_user_id,
                self.model.starts_at >= from_date,
                self.model.ends_at <= to_date,
            )
            result = await self.session.execute(query)
            model = result.scalars().all()
            return model
        except NoResultFound as ex:
            raise MeetingNotFoundException from ex



