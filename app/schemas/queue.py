from datetime import date

from pydantic import BaseModel


class QueueBase(BaseModel):
    name: str
    

class Queue(QueueBase):
    created_at: date


class QueueCreate(BaseModel):
    pass


class QueueUpdate(QueueBase):
    pass