from sqlalchemy import Boolean, Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from .. db import Base


class Stack(Base):
    __tablename__ = "stacks"
    id = Column(Integer, primary_key=True, index=True)
    # If users are a thing later on, then remove unique on just name,
    # and make a unique constrant on name and user_id
    name = Column(Text, unique=True, index=True)
    size = Column(Integer, default=0)

    cards = relationship("Card", back_populates="stack")
