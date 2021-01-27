from typing import List
from datetime import date

from pydantic import BaseModel


class CardDetailBase(BaseModel):
    card_id: int
    quality: int
    easiness: float
    interval: int
    repetitions: int
    last_review: date


class CardDetailCreate(CardDetailBase):
    pass


class CardDetail(CardDetailBase):
    id: int
    latest: bool
    next_review: date

    class Config:
        orm_mode = True
