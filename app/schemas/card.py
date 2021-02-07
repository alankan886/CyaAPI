from typing import List, Optional
from datetime import date

from pydantic import BaseModel


class CardBase(BaseModel):
    name: str
    stack_id: int
    quality: int
    prev_easiness: float
    prev_interval: int
    prev_repetitions: int
    prev_review_date: str


class CardBaseOptional(BaseModel):
    name: Optional[str]
    stack_id: Optional[int]
    quality: Optional[int]
    prev_easiness: Optional[float]
    prev_interval: Optional[int]
    prev_repetitions: Optional[int]
    prev_review_date: Optional[str]


class CardCreate(CardBase):
    pass


class CardOptionalAttrs(CardBaseOptional):
    pass


class Card(CardBase):
    id: int
    easiness: float
    interval: int
    repetitions: int
    review_date: str

    class Config:
        orm_mode = True
