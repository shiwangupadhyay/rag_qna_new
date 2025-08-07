from pydantic import BaseModel
from typing import List

# Input schema
class RunRequest(BaseModel):
    documents: str
    questions: List[str]

# output schema
class OutputSchema(BaseModel):
  answers: list[str]