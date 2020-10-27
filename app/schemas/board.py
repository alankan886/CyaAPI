from typing import List

from pydantic import BaseModel


class BoardBase(BaseModel):
    name: str
    size: int
    tags: List[str] = []


class BoardCreate(BoardBase):
    pass


class Board(BoardBase):
    id: int
    board_id: int

    class Config:
        orm_mode = True
