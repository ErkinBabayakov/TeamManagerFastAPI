from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime, timezone
from typing import List

from app.schemas.users import User


class Meeting(BaseModel):
    id: int
    title: str
    starts_at: datetime
    ends_at: datetime
    team_id: int
    organizer_id: int
    participant_ids: List[int] = []

    @field_validator("starts_at", "ends_at",mode='before')
    @classmethod
    def ensure_naive_datetime(cls, value: datetime) -> datetime:
        if isinstance(value, datetime) and value.tzinfo is not None:
            return value.astimezone(timezone.utc).replace(tzinfo=None)
        return value

    model_config = ConfigDict(from_attributes=True)

class MeetingRequestAdd(BaseModel):
    title: str
    starts_at: datetime
    ends_at: datetime
    participant_ids: List[int] = []

    @field_validator("starts_at", "ends_at", mode='before')
    @classmethod
    def ensure_naive_datetime(cls, value: datetime) -> datetime:
        if isinstance(value, datetime) and value.tzinfo is not None:
            return value.astimezone(timezone.utc).replace(tzinfo=None)
        return value

    model_config = ConfigDict(from_attributes=True)

class MeetingValidateTime(BaseModel):
    starts_at: datetime
    ends_at: datetime

    @field_validator("starts_at", "ends_at", mode='before')
    @classmethod
    def ensure_naive_datetime(cls, value: datetime) -> datetime:
        if isinstance(value, datetime) and value.tzinfo is not None:
            return value.astimezone(timezone.utc).replace(tzinfo=None)
        return value

class MeetingAdd(BaseModel):
    title: str
    starts_at: datetime
    ends_at: datetime
    team_id: int
    organizer_id: int

    @field_validator("starts_at", "ends_at", mode='before')
    @classmethod
    def ensure_naive_datetime(cls, value: datetime) -> datetime:
        if isinstance(value, datetime) and value.tzinfo is not None:
            return value.astimezone(timezone.utc).replace(tzinfo=None)
        return value

    model_config = ConfigDict(from_attributes=True)

class MeetingOut(BaseModel):
    title: str
    starts_at: datetime
    ends_at: datetime
    created_at: datetime
    participants: List[User]


    model_config = ConfigDict(from_attributes=True)