from app.models import MeetingParticipantOrm
from app.repositories.base import BaseRepository
from app.repositories.mappers.mappers import MeetingParticipantDataMapper


class MeetingParticipantRepository(BaseRepository):
    model = MeetingParticipantOrm
    mapper = MeetingParticipantDataMapper