from fastapi import HTTPException
from app.exceptions import UsersInMeetingsNotFoundException, TeamNotFoundException, UserNotFoundException, \
    MeetingNotFoundException, DataBaseException, ObjectNotFoundException
from app.models import MeetingOrm
from app.schemas.meetingparticipants import MeetingParticipant
from app.schemas.meetings import MeetingRequestAdd, MeetingAdd, MeetingValidateTime, MeetingOut
from app.services.base import BaseService

class MeetingsService(BaseService):
    """Сервисный слой для встреч"""

    async def create_meeting(self, team_id: int, organizer_id: int, meeting_data: MeetingRequestAdd):
        try:
            # Проверяем участников
            participants = await self.db.meetings.check_participants(participants_ids=meeting_data.participant_ids)
            if len(participants) != len(meeting_data.participant_ids):
                raise UsersInMeetingsNotFoundException

            for participant in participants:
                await self.db.meetings.check_member_participants(team_id=team_id, user_id= participant)

            meeting_validate_time = MeetingValidateTime(
                starts_at=meeting_data.starts_at,
                ends_at=meeting_data.ends_at,
            )

            for participant in participants:
                if await self.db.meetings.check_overlap(participant, meeting_validate_time.starts_at, meeting_validate_time.ends_at):
                    raise HTTPException(status_code=400, detail=f"Пользователь {participant} уже добавлен на встречу")

            meeting_add_data = MeetingAdd(
                title=meeting_data.title,
                starts_at=meeting_data.starts_at,
                ends_at=meeting_data.ends_at,
                team_id=team_id,
                organizer_id=organizer_id
            )
            db_data = await self.db.meetings.add(meeting_add_data)
            await self.db.flush()

            meeting_data_id = await self.db.meetings.get_one(id=db_data.id)

            # добавляем организатора как участника, если еще не добавлен
            all_participants = set(meeting_data.participant_ids)
            all_participants.add(organizer_id)
            for uid in all_participants:
                meeting_participants_data = MeetingParticipant(
                    meeting_id=meeting_data_id.id,
                    user_id=uid,
                )
                await self.db.meetingparticipants.add(meeting_participants_data)
            await self.db.commit()

            meeting_out_data = await self.db.meetings.get_meeting_data(all_participants)
            return f"Встреча создана, идентификатор встречи: {meeting_data_id.dict().get('id')}"

        except UsersInMeetingsNotFoundException:
            raise UsersInMeetingsNotFoundException
        except TeamNotFoundException:
            raise TeamNotFoundException
        except UserNotFoundException:
            raise UserNotFoundException


    async def cancel_meeting(self, meeting_id: int):
        try:
            meeting = await self.db.meetings.get_one(id=meeting_id)
            if not meeting:
                raise MeetingNotFoundException
            await self.db.meetings.delete(id=meeting_id)
            await self.db.commit()
        except DataBaseException:
            raise DataBaseException
        except ObjectNotFoundException:
            raise MeetingNotFoundException

    async def meeting_to_pydantic(self, meeting_orm: MeetingOrm) -> MeetingOut:
        participants = [mp.user for mp in meeting_orm.participants]
        return MeetingOut(
            title=meeting_orm.title,
            starts_at=meeting_orm.starts_at,
            ends_at=meeting_orm.ends_at,
            created_at=meeting_orm.created_at,
            participants=participants,
        )

    async def get_meetings(self, meeting_id: int):
        try:
            meeting = await self.db.meetings.get_meeting_with_participants(meeting_id=meeting_id)
            if not meeting:
                raise MeetingNotFoundException
            await self.db.commit()
            meeting_data = await self.meeting_to_pydantic(meeting)
            return meeting_data
        except DataBaseException:
            raise DataBaseException
        except ObjectNotFoundException:
            raise MeetingNotFoundException


