from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class QueueBase(BaseModel):
    name: str
    description: Optional[str]


class Queue(QueueBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class QueueCreate(QueueBase):
    pass


class QueueUpdate(QueueBase):
    pass
