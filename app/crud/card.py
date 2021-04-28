from datetime import date

from sqlalchemy.orm import Session
from supermemo2 import first_review, SMTwo

from .. import models
from .. schemas import Card, CardCreate, CardOptionalAttrs, CardNext
from . util import update_sm_two


def read_card_by_id(db: Session, card_id: int):
    return db.query(models.Card).filter(models.Card.id == card_id).first()


def read_card_by_name(db: Session, card_name: str):
    return db.query(models.Card).filter(models.Card.name == card_name).first()


def read_cards(db: Session):
    return db.query(models.Card).all()


def read_card_details_of_card(db: Session, card_id: int):
    return db.query(models.CardDetail).filter(models.CardDetail.card_id == card_id).all()


# TODO: I can probably just combine this with read_cards
def read_cards_due(db: Session, filter: str):
    # can handle more due dates later
    if filter == "today":
        due_date = date.today()

    return db.query(models.Card).filter(models.Card.review_date <= due_date).all()


def create_card(db: Session, card: CardCreate, is_first_review: bool):
    prev_review_date = card.prev_review_date if card.prev_review_date else None

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
    # attr value is attr where the autofill grabs values from for the /cards/{card_id}/next endpoint.
    # attr value equals to None means the attr isn't going to autofill
    update_attrs = [
        "name",
        "stack_id",
        "quality",
        "prev_easiness",
        "prev_interval",
        "prev_repetitions",
        "prev_review_date"
    ]
    for attr in update_attrs:
        existing_value = getattr(new_info, attr)
        if existing_value is not None:
            setattr(card, attr, existing_value)

    update_sm_two(card)
    db.commit()
    db.refresh(card)
    return card


def update_next_card(db: Session, card: Card, new_info: CardNext):
    # TODO: This needs more work on the naming, and probably remove quality out of update_attrs?
    update_attrs = {
        "quality": None,
        "prev_easiness": "easiness",
        "prev_interval": "interval",
        "prev_repetitions": "repetitions",
        "prev_review_date": "review_date"
    }
    for attr, prev_attr in update_attrs.items():
        existing_value = getattr(new_info, attr)
        # if autofill -> we autofill ez, int and rep. q actually must be there for autofill
        # also this shoudln't fill for review_date if it's in the body

        if existing_value is not None:
            setattr(card, attr, existing_value)
        elif prev_attr is not None:
            setattr(card, attr, getattr(card, prev_attr))

    update_sm_two(card)
    db.commit()
    db.refresh(card)
    return card


def delete_card(db: Session, card: Card):
    db.delete(card)
    db.commit()
