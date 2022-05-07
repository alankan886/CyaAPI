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
