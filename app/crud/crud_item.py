from sqlalchemy.orm import Session

from ..models.item import Item


def read_items(db: Session):
    return db.query(Item).all()
