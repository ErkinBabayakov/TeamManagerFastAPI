from pydantic import BaseModel, EmailStr,  ConfigDict
from enum import Enum
from typing import Optional


class UserRole(str, Enum):
    member = "member"
    manager = "manager"
    admin = "admin"

class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    role: Optional[UserRole] = UserRole.member

class UserAdd(BaseModel):
    email: EmailStr
    hashed_password: str
    first_name: str
    last_name: str
    role: Optional[UserRole] = UserRole.member


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    role: Optional[UserRole]

    model_config = ConfigDict(from_attributes=True)

class UserWithHashPassword(User):
    hashed_password: str

class UserCheckAdmin(User):
    role: UserRole


class UserEnter(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    password: str
    first_name: str
    last_name: str
    role: Optional[UserRole] = UserRole.member

class UserUpdateWithHashPassword(BaseModel):
    hashed_password: str
    first_name: str
    last_name: str
    role: Optional[UserRole] = UserRole.member

class UserPATCH(BaseModel):
    password: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    role: Optional[UserRole] | None = None

class UserPATCHUpdateWithoutHashPassword(BaseModel):
    first_name: str| None = None
    last_name: str| None = None
    role: Optional[UserRole] | None = None

class UserPATCHUpdateWithHashPassword(BaseModel):
    hashed_password: str
    first_name: str| None = None
    last_name: str| None = None
    role: Optional[UserRole] | None = None


class UserDelete(BaseModel):
    email: EmailStr

