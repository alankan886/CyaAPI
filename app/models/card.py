from typing import List
from datetime import date

from pydantic import BaseModel


class Card(BaseModel):
    name: str
    quality: int
    last_review: date
    next_review: date
    tags: List[str] = []
