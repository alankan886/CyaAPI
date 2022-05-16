import random
from datetime import date

from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.tests.utils.utils import random_lower_string
from app.tests.utils.queue import create_random_queue


def create_random_item(db: Session) -> models.Item:
    queue = create_random_queue(db)
    values = {
        "name": random_lower_string(),
        "quality": random.randrange(0, 6),
        "easiness": 2.5,
        "interval": 10,
        "repetitions": 1,
        "review_date": date.today(),
        "queue_id": queue.id,
    }
    item = schemas.ItemCreate(**values)
    return crud.create_item(db=db, item=item)
