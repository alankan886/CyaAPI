from typing import List
from datetime import date

from pydantic import BaseModel


class CardBase(BaseModel):
    name: str
    # quality: int
    # last_review: date
    # tags: List[str] = []


class CardCreate(CardBase):
    pass


class Card(CardBase):
    id: int
    board_id: int
    # next_review: date

    class Config:
        orm_mode = True
