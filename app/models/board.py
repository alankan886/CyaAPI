from typing import List

from pydantic import BaseModel


class Board(BaseModel):
    name: str
    size: int
    tags: List[str] = []
