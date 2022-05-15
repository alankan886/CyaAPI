from typing import Optional

from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.tests.utils.utils import random_lower_string


def create_random_queue(db: Session) -> models.Queue:
    name = random_lower_string()
    description = random_lower_string()
    queue = schemas.QueueCreate(name=name, description=description)
    return crud.create_queue(db=db, queue=queue)
