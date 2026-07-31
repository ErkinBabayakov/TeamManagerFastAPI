from pydantic import BaseModel, ConfigDict

class MeetingParticipant(BaseModel):
    meeting_id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)