from datetime import datetime
from enum import Enum
from sqlalchemy import ForeignKey, Enum as SQLEnum, Column, String

from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base

class UserRoles(str, Enum):
    member = "member"
    manager = "manager"
    admin = "admin"

class TeamMemberOrm(Base):
    __tablename__ = "team_members"
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    role = Column(SQLEnum(UserRoles), default=UserRoles.member)
    joined_at: Mapped[datetime] = mapped_column(default=datetime.now)

    team = relationship("TeamOrm", back_populates="members")
    user = relationship("UserOrm", back_populates="teams")