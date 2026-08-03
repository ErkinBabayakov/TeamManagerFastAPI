from datetime import datetime
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base

class EvaluationOrm(Base):
    __tablename__ = "evaluations"
    id: Mapped[int] = mapped_column(primary_key=True)
    score: Mapped[int] = mapped_column(nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=True)

    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"), unique=True, nullable=False)
    evaluator_id: Mapped[int] = mapped_column(ForeignKey("users.id"),  nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    task = relationship("TaskOrm", back_populates="evaluation")
    evaluator = relationship("UserOrm")