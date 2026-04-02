from pydantic import BaseModel
from typing import List, Optional

class Observation(BaseModel):
    ticket_id: int
    customer_query: str
    history: List[str]

class Action(BaseModel):
    action_type: str  # classify / respond / escalate
    content: Optional[str] = None

class Reward(BaseModel):
    score: float
    feedback: str