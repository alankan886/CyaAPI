from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .. extensions.db import Base


class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    board_id = Column(
        Integer,
        ForeignKey("boards.id", ondelete='CASCADE'),
        nullable=False
    )

    board = relationship("Board", back_populates="cards")
