from sqlalchemy.orm import Session
from supermemo2 import SMTwo

from ..schemas.item import Item, ItemCreate


def read_items(db: Session):
    return db.query(Item).all()

def read_item_in_queue_by_name(db: Session, item: Item):
    return db.query(Item).filter(Item.name == item.name, Item.queue_id == item.queue_id).first()


def create_item(db: Session, item: ItemCreate, is_first_review: bool):
    if is_first_review:
        sm_info = SMTwo().first_review(item.quality, item.review_date)
    else:
        sm_info = SMTwo().review(
            item.quality,
            item.prev_easiness,
            item.prev_interval,
            item.prev_repetitions,
            item.review_date
        )
    item_info = {**sm_info.dict(), "name": item.name, "queue_id": item.queue_id}
    db_item = Item(**item_info)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item