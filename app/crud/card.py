from sqlalchemy.orm import Session

from .. import models
from .. schemas import Card, CardCreate


def get_card(db: Session, card_id: int):
    return db.query(models.Card).filter(models.Card.id == card_id).first()


def get_cards(db: Session):
    return db.query(models.Card).all()


def create_card(db: Session, card: CardCreate, card_id: int, board_id: int):
    db_card = models.Card(**card.dict(), board_id=board_id)
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card
