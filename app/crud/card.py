from datetime import date

from sqlalchemy.orm import Session
from supermemo2 import first_review, SMTwo

from .. import models
from .. schemas import Card, CardCreate, CardOptionalAttrs
from ..util import convert_str_to_date


def read_card_by_id(db: Session, card_id: int):
    return db.query(models.Card).filter(models.Card.id == card_id).first()


def read_card_by_name(db: Session, card_name: str):
    return db.query(models.Card).filter(models.Card.name == card_name).first()


def read_cards(db: Session):
    return db.query(models.Card).all()


def read_card_details_of_card(db: Session, card_id: int):
    return db.query(models.CardDetail).filter(models.CardDetail.card_id == card_id).all()


def read_cards_due(db: Session, filter: str):
    # can handle more due dates later
    if filter == "today":
        due_date = date.today()

    return db.query(models.Card).order_by(models.Card.review_date <= due_date)


def create_card(db: Session, card: CardCreate, is_first_review: bool):
    prev_review_date = None
    if card.prev_review_date:
        prev_review_date = convert_str_to_date(card.prev_review_date)

    if is_first_review:
        sm_two = first_review(card.quality, prev_review_date)
    else:
        # might add an API method for calc as well to make this into 1 line
        sm_two = SMTwo()
        sm_two.calc(
            card.quality,
            card.prev_easiness,
            card.prev_interval,
            card.prev_repetitions,
            prev_review_date
        )

    card_info = {**sm_two.dict(), "name": card.name, "stack_id": card.stack_id}
    db_card = models.Card(**card_info)
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card


def update_card(db: Session, card: Card, new_info: CardOptionalAttrs):
    update_attrs = ["name", "stack_id", "quality", "prev_easiness", "prev_interval", "prev_repetitions", "prev_review_date"]
    for attr in update_attrs:
        value = getattr(new_info, attr)
        if value is not None:
            setattr(card, attr, getattr(new_info, attr))

    sm_two = SMTwo()
    sm_two.calc(
        card.quality,
        card.prev_easiness,
        card.prev_interval,
        card.prev_repetitions,
        convert_str_to_date(card.prev_review_date)
    )

    for name, value in sm_two.dict(curr=True).items():
        if name != "quality":
            setattr(card, name, value)

    db.commit()
    db.refresh(card)
    return card


def delete_card(db: Session, card: Card):
    db.delete(card)
    db.commit()
