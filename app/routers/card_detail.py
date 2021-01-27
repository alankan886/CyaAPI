from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from .. import crud, schemas
from ..db import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/{card_detail_id}")
def get_card_detail(card_detail_id: int, db: Session = Depends(get_db)):
    db_card = crud.read_card_detail_by_id(db, card_detail_id)
    if not db_card:
        raise HTTPException(status_code=404, detail=f"Card detail with id={card_detail_id} not found") 
    return db_card


@router.get("")
def get_card_details(db: Session = Depends(get_db)):
    db_card = crud.read_card_details(db)
    return db_card


@router.post("", status_code=201)
def post_card_detail(card_detail: schemas.CardDetailCreate, db: Session = Depends(get_db)):
    db_card_detail = crud.read_card_detail_by_card_id_and_review(db, card_detail)
    if db_card_detail:
        raise HTTPException(
            status_code=400,
            detail=f"Card detail with card_id={card_detail.card_id} and last_review date='{card_detail.last_review}' has already exists"
        )
    return crud.create_card_detail(db, card_detail)


@router.put("/{card_detail_id}")
def put_card_detail(card_detail_id: int, new_card_detail: schemas.CardDetailCreate, db: Session = Depends(get_db)):
    old_card_detail = crud.read_card_detail_by_id(db, card_detail_id)
    if not old_card_detail:
        return JSONResponse(status_code=201, content=crud.create_card_detail(db, new_card_detail))
    return crud.update_card_detail(db, old_card_detail, new_card_detail)


@router.delete("/{card_detail_id}")
def delete_card_detail(card_detail_id: int, db: Session = Depends(get_db)):
    db_card_detail = crud.read_card_detail_by_id(db, card_detail_id)
    if not db_card_detail:
        raise HTTPException(status_code=404, detail=f"Card detail with id={card_detail_id} is not found")
    crud.delete_card_detail(db, db_card_detail)
    return JSONResponse(status_code=204)
