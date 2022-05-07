from typing import List, Optional
from datetime import date

from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    stack_id: int
    quality: int


class Item(ItemBase):
    easiness: float
    interval: int
    repetitions: int
    review_date: date

class ItemCreate(ItemBase):
    easiness: Optional[float]
    interval: Optional[int]
    repetitions: Optional[int]
    review_date: Optional[date]
