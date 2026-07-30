from pydantic import BaseModel
from datetime import datetime
from typing import List

class Meeting(BaseModel):
    title: str
    starts_at: datetime
    ends_at: datetime
    participant_ids: List[int] = []