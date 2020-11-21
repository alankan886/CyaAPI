from fastapi import APIRouter, Depends, HTTPException

from .. import crud, schemas
from ..db import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.get('/{card_id}')
def read_card(card_id: int, db: Session = Depends(get_db)):
    db_card = crud.get_card_by_id(db, card_id)
    if not db_card:
        raise HTTPException(status_code=404, detail=f"Card with id={card_id} not found")
    return db_card


@router.get("")
def read_all_cards(db: Session = Depends(get_db)):
    db_cards = crud.get_cards(db)
    if not db_cards:
        raise HTTPException(status_code=404, detail="No cards are found")
    return db_cards


@router.post("")
def create_card(card: schemas.CardCreate, db: Session = Depends(get_db)):
    db_card = crud.get_card_by_name(db, card.name)
    if db_card:
        raise HTTPException(status_code=400, detail=f"Card with the name {card.name} has already exists")
    return crud.create_card(db, card)


# TODO: Refactor the name so it's not delete or remove when they should just be the same
@router.delete('/{card_id}')
def delete_card(card_id: int, db: Session = Depends(get_db)):
    db_card = crud.get_card_by_id(db, card_id)
    if not db_card:
        raise HTTPException(status_code=404, detail=f"Card with id={card_id} is not found")
    return crud.delete_card(db, db_card)
