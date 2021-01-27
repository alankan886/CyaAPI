from sqlalchemy import Column, Integer, Float, Date, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from .. db import Base


class CardDetail(Base):
    __tablename__ = "cards_details"
    id = Column(Integer, primary_key=True, index=True)
    quality = Column(Integer)
    easiness = Column(Float)
    interval = Column(Integer)
    repetitions = Column(Integer)
    last_review = Column(Date)
    next_review = Column(Date)
    latest = Column(Boolean)
    card_id = Column(
        Integer,
        ForeignKey("cards.id", ondelete='CASCADE'),
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint("card_id", "last_review", "next_review", name='_card_id_last_review_next_review_uc'),
    )
    card = relationship("Card", back_populates="card_details")
