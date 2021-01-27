from sqlalchemy.orm import Session

from .. import models
from .. schemas import Card, CardCreate


def read_card_by_id(db: Session, card_id: int):
    return db.query(models.Card).filter(models.Card.id == card_id).first()


def read_card_by_name(db: Session, card_name: str):
    return db.query(models.Card).filter(models.Card.name == card_name).first()


def read_cards(db: Session):
    return db.query(models.Card).all()


def read_card_details_of_card(db: Session, card_id: int):
    return db.query(models.CardDetail).filter(models.CardDetail.card_id == card_id).all()


# I think I need to add a field to mark if the record is the latest
# and it's possible we can just replace this with the existing read_cards
# def read_card_due(db: Session, card_id: int):
#     card_detail = db.query(models.CardDetail).order_by(models.CardDetail.last_review.desc())
#     return


def update_card(db: Session, old_card: Card, new_card: CardCreate):
    old_card.name = new_card.name
    db.commit()
    db.refresh(old_card)
    return old_card


def create_card(db: Session, card: CardCreate):
    db_card = models.Card(**card.dict())
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card


def delete_card(db: Session, card: Card):
    db.delete(card)
    db.commit()
