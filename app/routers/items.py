from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import crud, schemas
from ..db import get_db

router = APIRouter(
    prefix="/items",
    tags=["Items"],
)


@router.get("/", response_model=List[schemas.Item])
async def read_items(today: bool = False, db: Session = Depends(get_db)):
    return crud.read_items(db, today)


@router.post("/", status_code=201, response_model=schemas.Item)
async def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    if crud.read_item_in_queue_by_name(item):
        raise HTTPException(
            status_code=400,
            detail=f"Item with the name '{item.name}' has already exists in Queue '{item.queue}'",
        )

    return crud.create_item(db, item, False)


@router.post("/first-review/", status_code=201, response_model=schemas.Item)
async def create_first_review_item(item: schemas.ItemReview, db: Session = Depends(get_db)):
    if crud.read_item_in_queue_by_name(item):
        raise HTTPException(
            status_code=400,
            detail=f"Item with the name '{item.name}' has already exists in Queue '{item.queue}'",
        )

    return crud.create_item(db, item, True)


@router.patch("/{item_id}/", response_model=schemas.Item)
async def update_item(
    item_id: str, new_info: schemas.ItemPartialUpdate, db: Session = Depends(get_db)
):
    db_item = crud.read_item_by_id(db, item_id)
    if crud.read_item_in_queue_by_id(item_id):
        raise HTTPException(
            status_code=404, detail=f"Item with the id='{item_id}' is not found"
        )

    return crud.update_item(db, db_item, new_info)


@router.put("/{item_id}/review/", response_model=schemas.Item)
async def review_item(
    item_id: str, new_info: schemas.ItemReview, db: Session = Depends(get_db)
):
    db_item = crud.read_item_by_id(db, item_id)
    if crud.read_item_in_queue_by_id(item_id):
        raise HTTPException(
            status_code=404, detail=f"Item with the id='{item_id}' is not found"
        )

    return crud.review_card(db, db_item, new_info.quality, new_info.review_date)


@router.delete("/{item_id}/")
async def remove_item(item_id: str, db: Session = Depends(get_db)):
    db_item = crud.read_item_by_id(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail=f"Item with id='{item_id}' is not found")
    
    crud.delete_item(db, db_item)

    return JSONResponse(status_code=204)
