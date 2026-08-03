from enum import Enum
from datetime import datetime
from sqlalchemy import String, ForeignKey, Column, Text, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class TaskStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    done = "done"

class TaskOrm(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.open)
    due_date: Mapped[datetime] = mapped_column(nullable=True)

    team_id: Mapped[int] = mapped_column(ForeignKey('teams.id'))
    creator_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    assignee_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    team = relationship("TeamOrm", back_populates="tasks")
    creator = relationship("UserOrm", foreign_keys=[creator_id], back_populates="created_tasks")
    assignee = relationship("UserOrm", foreign_keys=[assignee_id], back_populates="assigned_tasks")
    comments = relationship("CommentOrm", back_populates="task", cascade="all, delete-orphan")
    evaluation = relationship("EvaluationOrm", back_populates="task", uselist=False, cascade="all, delete-orphan")

