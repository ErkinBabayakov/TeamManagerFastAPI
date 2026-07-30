from datetime import datetime
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base

class MeetingOrm(Base):
    __tablename__ = "meetings"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    starts_at: Mapped[datetime] = mapped_column(nullable=False)
    ends_at: Mapped[datetime] = mapped_column(nullable=False)

    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    organizer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    team = relationship("TeamOrm", back_populates="meetings")
    organizer = relationship("UserOrm")
    participants = relationship("MeetingParticipantOrm", back_populates="meeting")

class MeetingParticipantOrm(Base):
    __tablename__ = "meeting_participants"
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meetings.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    joined_at: Mapped[datetime] = mapped_column(default=datetime.now)

    meeting = relationship("MeetingOrm", back_populates="participants")
    user = relationship("UserOrm", back_populates="meetings")