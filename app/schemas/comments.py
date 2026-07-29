from pydantic import BaseModel, ConfigDict

class Comment(BaseModel):
    id: int
    text: str
    task_id: int
    author_id: int

    model_config = ConfigDict(from_attributes=True)

class CommentRequestAdd(BaseModel):
    text: str

class CommentAdd(BaseModel):
    text: str
    task_id: int
    author_id: int
