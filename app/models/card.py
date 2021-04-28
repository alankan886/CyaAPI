from sqlalchemy import Boolean, Column, ForeignKey, Integer, Text, UniqueConstraint, Float, Date
from sqlalchemy.orm import relationship

from .. db import Base


class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, index=True)
    stack_id = Column(
        Integer,
        ForeignKey("stacks.id", ondelete='CASCADE'),
        nullable=False
    )
    quality = Column(Integer)
    prev_easiness = Column(Float)
    easiness = Column(Float)
    prev_interval = Column(Integer)
    interval = Column(Integer)
    prev_repetitions = Column(Integer)
    repetitions = Column(Integer)
    prev_review_date = Column(Date)
    review_date = Column(Date)

    __table_args__ = (
        UniqueConstraint("name", "stack_id", name='_name_stack_id_uc'),
    )
    stack = relationship("Stack", back_populates="cards")
