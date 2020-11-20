from sqlalchemy.orm import Session

from .. import models
from .. schemas import Card, CardCreate


def get_card_by_id(db: Session, card_id: int):
    return db.query(models.Card).filter(models.Card.id == card_id).first()


def get_card_by_name(db: Session, card_name: str):
    return db.query(models.Card).filter(models.Card.name == card_name).first()


def get_cards(db: Session):
    return db.query(models.Card).all()


def create_card(db: Session, card: CardCreate):
    db_card = models.Card(**card.dict())
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card


def delete_card(db: Session, card: Card):
    db.delete(card)
    db.commit()
