from fastapi import APIRouter, Depends, HTTPException

from .. import crud, schemas
from ..db import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.get('/{card_details_id}')
def read_card_details(card_details_id: int, db: Session = Depends(get_db)):
    db_card = crud.get_card_details_by_id(db, card_details_id)
    if not db_card:
        raise HTTPException(status_code=404, detail=f"Card details with id={card_details_id} not found")
    return db_card
