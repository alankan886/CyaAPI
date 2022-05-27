from typing import List
from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Item])
async def read_items(today: bool = False, db: Session = Depends(get_db)):
    return crud.read_items(db, today)


@router.post("/", status_code=201, response_model=schemas.Item)
async def create_item(
    item: schemas.ItemCreate,
    first_review_values: bool = False,
    db: Session = Depends(get_db),
):
    if not first_review_values and not (
        item.easiness and item.interval and item.repetitions
    ):
        raise HTTPException(
            status_code=400,
            detail=f"Use first review values or provide easiness, interval and repetitions",
        )

    if first_review_values:
        item.easiness = 2.5
        item.interval = 0
        item.repetitions = 0

    if not item.review_date:
        item.review_date = date.today()

    if crud.read_item_in_queue_by_name(db, item):
        raise HTTPException(
            status_code=400,
            detail=f"Item with the name '{item.name}' has already exists in Queue '{item.queue_id}'",
        )

    return crud.create_item(db, item)


@router.patch("/{item_id}/", response_model=schemas.Item)
async def update_item(
    item_id: str, new_info: schemas.ItemPartialUpdate, db: Session = Depends(get_db)
):
    db_item = crud.read_item_by_id(db, item_id)
    if not db_item:
        raise HTTPException(
            status_code=404, detail=f"Item with the id='{item_id}' is not found"
        )

    return crud.update_item(db, db_item, new_info)


@router.patch("/{item_id}/review/", response_model=schemas.Item)
async def review_item(
    item_id: str, new_info: schemas.ItemReview, db: Session = Depends(get_db)
):
    db_item = crud.read_item_by_id(db, item_id)
    if not db_item:
        raise HTTPException(
            status_code=404, detail=f"Item with the id='{item_id}' is not found"
        )

    return crud.review_item(db, db_item, new_info.quality, new_info.review_date)


@router.delete("/{item_id}/")
async def remove_item(item_id: str, db: Session = Depends(get_db)):
    db_item = crud.read_item_by_id(db, item_id)
    if not db_item:
        raise HTTPException(
            status_code=404, detail=f"Item with the id='{item_id}' is not found"
        )

    crud.delete_item(db, db_item)

    return JSONResponse(status_code=204)
