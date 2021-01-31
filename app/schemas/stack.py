from typing import List

from pydantic import BaseModel

from .card import Card


class StackBase(BaseModel):
    name: str


class StackCreate(StackBase):
    pass


class Stack(StackBase):
    id: int
    cards: List[Card]

    class Config:
        orm_mode = True
