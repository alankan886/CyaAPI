from typing import Optional, List

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


@router.get("", response_model=List[schemas.Card])
def get_cards(filter: Optional[str] = None, db: Session = Depends(get_db)):
    if filter:
        db_cards = crud.read_cards_due(db, filter)
    else:
        db_cards = crud.read_cards(db)

    # TODO: might not need this
    if not db_cards:
        return []
    return db_cards


@router.post("", status_code=201)
def post_card(card: schemas.CardCreate, db: Session = Depends(get_db)):
    db_card = crud.read_card_by_name(db, card.name)
    if db_card:
        raise HTTPException(status_code=400, detail=f"Card with the name {card.name} has already exists")
    return crud.create_card(db, card, False)


@router.post("/first-review", status_code=201)
def post_first_review_card(card: schemas.CardCreateFirstReview, db: Session = Depends(get_db)):
    db_card = crud.read_card_by_name(db, card.name)
    if db_card:
        raise HTTPException(status_code=400, detail=f"Card with the name {card.name} has already exists")
    return crud.create_card(db, card, True)


@router.patch("/{card_id}")
def patch_card(card_id: int, new_info: schemas.CardOptionalAttrs, db: Session = Depends(get_db)):
    db_card = crud.read_card_by_id(db, card_id)
    if not db_card:
        return JSONResponse(status_code=201, content=crud.create_card(db, new_info))
    return crud.update_card(db, db_card, new_info)


@router.patch("/{card_id}/review")
def patch_next_card(card_id: int, new_info: schemas.CardReview, db: Session = Depends(get_db)):
    db_card = crud.read_card_by_id(db, card_id)
    if not db_card:
        return HTTPException(status_code=404, detail=f"Card with id={card_id} not found")
    return crud.update_next_card(db, db_card, new_info)


@router.delete('/{card_id}')
def delete_card(card_id: int, db: Session = Depends(get_db)):
    db_card = crud.read_card_by_id(db, card_id)
    if not db_card:
        raise HTTPException(status_code=404, detail=f"Card with id={card_id} not found")
    crud.delete_card(db, db_card)
    return JSONResponse(status_code=204)
