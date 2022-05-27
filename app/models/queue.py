from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.orm import relationship

from ..db import Base


class Queue(Base):
    __tablename__ = "queues"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, index=True)
    description = Column(Text)
    created_at = Column(DateTime)

    items = relationship("Item", back_populates="queue")
