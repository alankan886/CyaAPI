from sqlalchemy.orm import Session

from .. import models
from .. schemas import Stack, StackCreate


def read_stack_by_id(db: Session, stack_id: int):
    return db.query(models.Stack).filter(models.Stack.id == stack_id).first()


def read_stack_by_name(db: Session, stack_name: str):
    return db.query(models.Stack).filter(models.Stack.name == stack_name).first()


def read_stacks(db: Session):
    return db.query(models.Stack).all()


def read_cards_in_stacks(db: Session, stack_id: int):
    return db.query(models.Card).filter(models.Card.stack_id == stack_id).all()


def create_stack(db: Session, stack: StackCreate):
    db_stack = models.Stack(name=stack.name)
    db.add(db_stack)
    db.commit()
    db.refresh(db_stack)
    return db_stack


def update_stack(db: Session, stack: Stack, new_info: StackCreate):
    stack.name = new_info.name
    db.commit()
    db.refresh(stack)
    return stack


def delete_stack(db: Session, stack: Stack):
    db.delete(stack)
    db.commit()
