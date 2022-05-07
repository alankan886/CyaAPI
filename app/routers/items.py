from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from ..db import get_db

router = APIRouter(
    prefix="/items", tags=["items"], responses={404: {"description": "Not found"}}
)


@router.get("/", response_model=List[schemas.Item])
async def read_items(db: Session = Depends(get_db)):
    return crud.read_items(db)


@router.post("/", status_code=201, response_model=schemas.Item)
async def create_item():
    return {"hello": "world"}


@router.post("/first-review", status_code=201, response_model=schemas.Item)
async def create_first_review_item():
    return {"hello": "world"}


@router.put("/{item_id}", response_model=schemas.Item)
async def update_item(item_id: str):
    return {"hello": "world"}


@router.put("/{item_id}/review", response_model=schemas.Item)
async def review_item(item_id: str):
    return {"hello": "world"}


@router.delete("/{item_id}")
async def remove_item(item_id: str):
    return {"hello": "world"}
