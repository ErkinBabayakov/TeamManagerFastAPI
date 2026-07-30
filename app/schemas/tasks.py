from enum import Enum
from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional

class TaskStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    done = "done"

class Task(BaseModel):
    id: int
    title: str
    description: str
    status: Optional[TaskStatus]
    due_date: datetime

    team_id: int
    creator_id: int
    assignee_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TaskRequestAdd(BaseModel):
    title: str
    description: str | None = None
    due_date: datetime | None = None
    assignee_id: int | None = None


class TaskAdd(BaseModel):
    title: str
    description: str | None = None
    due_date: datetime | None = None
    team_id: int
    creator_id: int
    assignee_id: int | None = None

    @field_validator("due_date", mode='before')
    @classmethod
    def ensure_naive_datetime(cls, value: datetime) -> datetime:
        if isinstance(value, datetime) and value.tzinfo is not None:
            return value.astimezone(timezone.utc).replace(tzinfo=None)
        return value

class TaskPATCH(BaseModel):
    title: str | None = None
    description: str | None = None
    status: Optional[TaskStatus] | None = None
    due_date: datetime | None = None
    assignee_id: int | None = None

    @field_validator("due_date", mode='before')
    @classmethod
    def ensure_naive_datetime(cls, value: datetime) -> datetime:
        if isinstance(value, datetime) and value.tzinfo is not None:
            return value.astimezone(timezone.utc).replace(tzinfo=None)
        return value

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: Optional[TaskStatus] | None = None
    due_date: datetime | None = None
    assignee_id: int | None = None

    @field_validator("due_date", mode='before')
    @classmethod
    def ensure_naive_datetime(cls, value: datetime) -> datetime:
        if isinstance(value, datetime) and value.tzinfo is not None:
            return value.astimezone(timezone.utc).replace(tzinfo=None)
        return value

class TaskResponse(BaseModel):
    title: str




