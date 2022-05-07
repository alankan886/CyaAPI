from sqlalchemy import Column, Integer, Text, ForeignKey, Float, Date
from sqlalchemy.orm import relationship

from ..db import Base


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, index=True)
    queue_id = Column(
        Integer, ForeignKey("queues.id", ondelete="CASCADE"), nullable=False
    )
    quality = Column(Integer)
    easiness = Column(Float)
    interval = Column(Integer)
    repetitions = Column(Integer)
    review_date = Column(Date)

    queue = relationship("Queue", back_populates="items")
