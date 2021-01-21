from typing import List
from datetime import date

from pydantic import BaseModel


class CardDetailsBase(BaseModel):
    name: str
    card_id: int
    quality: int
    easiness: float
    interval: int
    repetitions: int
    last_review: date
    next_review: date


class CardDetailsCreate(CardDetailsBase):
    pass


class CardDetails(CardDetailsBase):
    id: int

    class Config:
        orm_mode = True
