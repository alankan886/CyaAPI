from sqlalchemy.orm import Session
from datetime import date, datetime
from supermemo2 import SMTwo

from app import models, schemas


def read_items(db: Session, today: bool):
    if today:
        return (
            db.query(models.Item).filter(models.Item.review_date <= date.today()).all()
        )

    return db.query(models.Item).all()


def read_item_in_queue_by_name(db: Session, item: schemas.Item):
    return (
        db.query(models.Item)
        .filter(models.Item.name == item.name, models.Item.queue_id == item.queue_id)
        .count()
    )


def read_item_by_id(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def create_item(db: Session, item: schemas.ItemCreate):
    item_info = {
        "name": item.name,
        "queue_id": item.queue_id,
        "quality": item.quality,
        "easiness": item.easiness,
        "interval": item.interval,
        "repetitions": item.repetitions,
        "review_date": item.review_date,
        "created_at": datetime.now(),
    }
    db_item = models.Item(**item_info)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item


def update_item(db: Session, item: schemas.Item, new_info: schemas.ItemPartialUpdate):
    update_attrs = [
        "name",
        "queue_id",
        "quality",
        "easiness",
        "interval",
        "repetitions",
        "review_date",
    ]

    for attr in update_attrs:
        new_value = getattr(new_info, attr)
        if new_value:
            setattr(item, attr, new_value)

    db.commit()
    db.refresh(item)

    return item


def review_item(db: Session, item: schemas.Item, quality: int, review_date: date):
    update_attrs = ["easiness", "interval", "repetitions", "review_date"]
    item.quality = quality

    # TODO: perhaps take this block out code and put it into endpoints code
    # keep the crud code closely relate to DB actions
    if not review_date:
        review_date = item.review_date

    review_info = SMTwo(item.easiness, item.interval, item.repetitions).review(
        quality, review_date
    )
    for attr in update_attrs:
        new_value = getattr(review_info, attr)
        setattr(item, attr, new_value)

    db.commit()
    db.refresh(item)

    return item


def delete_item(db: Session, item: schemas.Item):
    db.delete(item)
    db.commit()
