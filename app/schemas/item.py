from typing import Optional
from datetime import date

from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    stack_id: int
    quality: int


class Item(ItemBase):
    id: int
    easiness: float
    interval: int
    repetitions: int
    review_date: date
    created_at: date

    class Config:
        orm_mode = True


class ItemCreate(ItemBase):
    easiness: float
    interval: int
    repetitions: int
    review_date: date


class ItemPartialUpdate(BaseModel):
    name: Optional[str]
    stack_id: Optional[int]
    quality: Optional[int]
    easiness: Optional[float]
    interval: Optional[int]
    repetitions: Optional[int]
    review_date: Optional[date]


class ItemReview(BaseModel):
    quality: int
    review_date: Optional[date]
