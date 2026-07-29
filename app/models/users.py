from enum import Enum
from sqlalchemy import String, Enum as SQLEnum, Column
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class UserRole(str, Enum):
    member = "member"
    manager = "manager"
    admin = "admin"

class UserOrm(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(200), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    role = Column(SQLEnum(UserRole), default=UserRole.member)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    created_teams = relationship("TeamOrm", back_populates="creator")
    teams = relationship("TeamMemberOrm", back_populates="user")
    created_tasks = relationship("TaskOrm", foreign_keys="TaskOrm.creator_id", back_populates="creator")
    assigned_tasks = relationship("TaskOrm", foreign_keys="TaskOrm.assignee_id", back_populates="assignee")




