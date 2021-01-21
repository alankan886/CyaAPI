from sqlalchemy.orm import Session

from .. import models
from .. schemas import CardDetails, CardDetailsCreate


# name it CRUD and name endpoints with HTTP name
def get_card_detail_by_id(db: Session, card_detail_id: int):
    return db.query(models.CardDetails).filter(models.CardDetails.id == card_detail_id).first()


def get_card_details_by_board_id(db: Session, board_id: int):
    return db.query(models.CardDetails).filter(models.CardDetails.board_id == board_id).first()
