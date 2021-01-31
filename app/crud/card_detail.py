from datetime import datetime

from sqlalchemy.orm import Session
from supermemo2 import first_review

from .. import models
from .. schemas import CardDetail, CardDetailCreate


def read_card_detail_by_id(db: Session, card_detail_id: int):
    return db.query(models.CardDetail).filter(models.CardDetail.id == card_detail_id).first()


def read_card_detail_by_card_id_and_review(db: Session, card_detail: CardDetailCreate):
    return db.query(
        models.CardDetail).filter(
            models.CardDetail.card_id == card_detail.card_id,
            models.CardDetail.last_review == card_detail.last_review
    ).first()


def read_card_details(db: Session):
    return db.query(models.CardDetail).all()


# TODO: use supermemo2 to calc next_review
def create_card_detail(db: Session, card_detail: CardDetailCreate):
    # TODO: handle setting the latest field to true or false
    card_detail_dict = card_detail.dict()
    card_detail_dict["next_review"] = first_review(card_detail.quality, card_detail.last_review).review_date
    card_detail_dict["latest"] = True
    db_card_detail = models.CardDetail(**card_detail_dict)
    db.add(db_card_detail)
    db.commit()
    db.refresh(db_card_detail)
    return db_card_detail


# TODO: If any values changed, call supermemo2 to update the next review date
def update_card_detail(db: Session, old_card_detail: CardDetail, new_card_detail: CardDetailCreate):
    attrs = ["quality", "easiness", "interval", "repetitions", "last_review", "card_id"]
    for attr in attrs:
        setattr(old_card_detail, attr, getattr(new_card_detail, attr))
    db.commit()
    db.refresh(old_card_detail)
    return old_card_detail


def delete_card_detail(db: Session, card_detail: CardDetail):
    db.delete(card_detail)
    db.commit()
