from sqlalchemy import Column, Integer, Text, Date
from sqlalchemy.orm import relationship

from ..db import Base


class Queue(Base):
    __tablename__ = "queues"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, index=True)
    created_at = Column(Date)

    items = relationship("Item", back_populates="queue")
