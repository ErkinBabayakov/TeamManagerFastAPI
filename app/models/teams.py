from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.database import Base


class TeamOrm(Base):
    __tablename__ = "teams"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    invite_code: Mapped[str] = mapped_column(String(100), unique=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    creator = relationship("UserOrm", back_populates="created_teams")
    members = relationship("TeamMemberOrm", back_populates="team")
    tasks = relationship("TaskOrm", back_populates="team")