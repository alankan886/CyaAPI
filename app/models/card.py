from sqlalchemy import Boolean, Column, ForeignKey, Integer, Text, UniqueConstraint
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

    __table_args__ = (
        UniqueConstraint("name", "stack_id", name='_name_stack_id_uc'),
    )
    stack = relationship("Stack", back_populates="cards")
    card_details = relationship("CardDetail", back_populates="card")
