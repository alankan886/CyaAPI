from sqlalchemy.orm import Session
from datetime import date, datetime

from app import models, schemas


def read_queues(db: Session):
    return db.query(models.Queue).all()


def read_queue_by_name(db: Session, queue: schemas.Queue):
    return (
        db.query(models.Queue)
        .filter(models.Queue.name == queue.name)
        .first()
    )


def read_queue_by_id(db: Session, item_id: int):
    return db.query(models.Queue).filter(models.Queue.id == item_id).first()


def create_queue(db: Session, queue: schemas.QueueCreate):
    db_queue = models.Queue(name=queue.name, created_at=datetime.now())
    db.add(db_queue)
    db.commit()
    db.refresh(db_queue)

    return db_queue


def update_queue(db: Session, queue: schemas.Queue, new_info: schemas.QueueUpdate):
    update_attrs = [
        "name",
    ]

    for attr in update_attrs:
        new_value = getattr(new_info, attr)
        if new_value:
            setattr(queue, attr, new_value)

    db.commit()
    db.refresh(queue)

    return queue


def delete_queue(db: Session, queue: schemas.Queue):
    db.delete(queue)
    db.commit()