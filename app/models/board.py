from sqlalchemy import Boolean, Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from .. db import Base


class Board(Base):
    __tablename__ = "boards"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, unique=True, index=True)
    size = Column(Integer, default=0)

    cards = relationship("Card", back_populates="board")
