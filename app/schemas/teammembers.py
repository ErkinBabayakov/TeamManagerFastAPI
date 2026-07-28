from pydantic import BaseModel, ConfigDict
from enum import Enum
from datetime import datetime

class UserRole(str, Enum):
    member = "member"
    manager = "manager"
    admin = "admin"

class TeamMember(BaseModel):
    team_id: int
    user_id: int
    first_name: str
    last_name: str
    role: UserRole
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TeamMemberAdd(BaseModel):
    team_id: int
    user_id: int
    first_name: str
    last_name: str
    role: UserRole

class TeamMemberPATCH(BaseModel):
    team_id: int
    user_id: int
    role: UserRole

class TeamMemberPATCHRole(BaseModel):
    role: UserRole

class JoinTeam(BaseModel):
    invite_code: str
    first_name: str
    last_name: str
    role: UserRole
