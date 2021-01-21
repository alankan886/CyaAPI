from sqlalchemy import Boolean, Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from .. db import Base


class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, unique=True, index=True)

    stack_id = Column(
        Integer,
        ForeignKey("stacks.id", ondelete='CASCADE'),
        nullable=False
    )

    stack = relationship("Stack", back_populates="cards")
