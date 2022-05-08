from sqlalchemy.orm import Session
from datetime import date
from supermemo2 import SMTwo

from ..schemas.item import Item, ItemCreate, ItemPartialUpdate


def read_items(db: Session):
    return db.query(Item).all()


def read_item_in_queue_by_name(db: Session, item: Item):
    return (
        db.query(Item)
        .filter(Item.name == item.name, Item.queue_id == item.queue_id)
        .first()
    )


def read_card_by_id(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()


def create_item(db: Session, item: ItemCreate, is_first_review: bool):
    if is_first_review:
        review_info = SMTwo.first_review(item.quality, item.review_date)
    else:
        review_info = SMTwo(
            item.easiness, item.prev_interval, item.prev_repetitions
        ).review(item.quality, item.review_date)

    item_info = {**review_info.dict(), "name": item.name, "queue_id": item.queue_id}
    db_item = Item(**item_info)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item


def update_item(db: Session, item: Item, new_info: ItemPartialUpdate):
    update_attrs = [
        "name",
        "stack_id",
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


def review_card(db: Session, item: Item, quality: int, review_date: date):
    update_attrs = ["quality", "easiness", "interval", "repetitions", "review_date"]

    if not review_date:
        review_date = item.review_date

    review_info = SMTwo(
        item.easiness, item.prev_interval, item.prev_repetitions
    ).review(quality, review_date)
    for attr in update_attrs:
        new_value = getattr(review_info, attr)
        setattr(item, attr, new_value)

    db.commit()
    db.refresh(item)

    return item


def delete_item(db: Session, item: Item):
    db.delete(item)
    db.commit()
