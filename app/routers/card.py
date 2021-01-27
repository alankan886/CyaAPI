from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from .. import crud, schemas
from ..db import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.get('/{card_id}')
def get_card(card_id: int, db: Session = Depends(get_db)):
    db_card = crud.read_card_by_id(db, card_id)
    if not db_card:
        raise HTTPException(status_code=404, detail=f"Card with id={card_id} not found")
    return db_card


@router.get("")
def get_cards(db: Session = Depends(get_db)):
    db_cards = crud.read_cards(db)
    if not db_cards:
        return []
    return db_cards


@router.get('/{card_id}/card_details')
def get_card_details_of_card(card_id: int, db: Session = Depends(get_db)):
    card_details = crud.read_card_details_of_card(db, card_id)
    return card_details


@router.post("", status_code=201)
def post_card(card: schemas.CardCreate, db: Session = Depends(get_db)):
    db_card = crud.read_card_by_name(db, card.name)
    if db_card:
        raise HTTPException(status_code=400, detail=f"Card with the name {card.name} has already exists")
    return crud.create_card(db, card)


@router.put("/{card_id}")
def put_card(card_id: int, new_card: schemas.CardCreate, db: Session = Depends(get_db)):
    old_card = crud.read_card_by_id(db, card_id)
    if not old_card:
        return JSONResponse(status_code=201, content=crud.create_card(db, new_card))
    return crud.update_card(db, old_card=old_card, new_card=new_card)


@router.delete('/{card_id}')
def delete_card(card_id: int, db: Session = Depends(get_db)):
    db_card = crud.read_card_by_id(db, card_id)
    if not db_card:
        raise HTTPException(status_code=404, detail=f"Card with id={card_id} is not found")
    crud.delete_card(db, db_card)
    return JSONResponse(status_code=204)
