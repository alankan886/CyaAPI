from typing import List

from pydantic import BaseModel

from .card import Card


class BoardBase(BaseModel):
    name: str


class BoardCreate(BoardBase):
    pass


class Board(BoardBase):
    id: int
    size: int
    cards: List[Card]

    class Config:
        orm_mode = True
