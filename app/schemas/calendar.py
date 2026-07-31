from typing import Optional
from pydantic import BaseModel, field_validator
from datetime import datetime, timezone

class CalendarEvent(BaseModel):
    id: int
    title: str
    start: datetime
    end: datetime
    type: str  # "task" or "meeting"
    status: Optional[str] = None

    @field_validator("start", "end", mode='before')
    @classmethod
    def ensure_naive_datetime(cls, value: datetime) -> datetime:
        if isinstance(value, datetime) and value.tzinfo is not None:
            return value.astimezone(timezone.utc).replace(tzinfo=None)
        return value

class CalendarEventValidateDate(BaseModel):
    start: datetime
    end: datetime

    @field_validator("start", "end", mode='before')
    @classmethod
    def ensure_naive_datetime(cls, value: datetime) -> datetime:
        if isinstance(value, datetime) and value.tzinfo is not None:
            return value.astimezone(timezone.utc).replace(tzinfo=None)
        return value