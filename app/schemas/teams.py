from pydantic import BaseModel, ConfigDict
from datetime import datetime

class Team(BaseModel):
    id: int
    name: str
    invite_code: str
    creator_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TeamAdd(BaseModel):
    name: str
    invite_code: str
    creator_id: int


class TeamRequestAdd(BaseModel):
    name: str


