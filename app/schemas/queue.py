from typing import Optional
from datetime import date

from pydantic import BaseModel


class QueueBase(BaseModel):
    name: str
    description: Optional[str]


class Queue(QueueBase):
    id: int
    created_at: date

    class Config:
        orm_mode = True


class QueueCreate(QueueBase):
    pass


class QueueUpdate(QueueBase):
    pass
