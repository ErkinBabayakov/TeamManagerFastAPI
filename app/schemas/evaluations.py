from pydantic import BaseModel, Field, ConfigDict


class Evaluation(BaseModel):
    id: int
    score: int = Field(..., ge=1, le=5)
    comment: str | None = None
    task_id: int
    evaluator_id: int

    model_config = ConfigDict(from_attributes=True)

class EvaluationRequestAdd(BaseModel):
    score: int = Field(..., ge=1, le=5, description="Поставить оценку от 1 до 5")
    comment: str | None = None

class EvaluationAdd(BaseModel):
    score: int = Field(..., ge=1, le=5)
    comment: str | None = None
    task_id: int
    evaluator_id: int






