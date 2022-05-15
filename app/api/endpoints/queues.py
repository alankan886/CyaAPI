from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Queue])
async def read_queues(db: Session = Depends(get_db)):
    return crud.read_queues(db)


@router.post("/", status_code=201, response_model=schemas.Queue)
async def create_queue(queue: schemas.QueueCreate, db: Session = Depends(get_db)):
    if crud.read_queue_by_name(db, queue):
        raise HTTPException(
            status_code=400,
            detail=f"Queue with the name '{queue.name}' has already exists",
        )

    return crud.create_queue(db, queue)


@router.put("/{queue_id}", response_model=schemas.Queue)
async def update_queue(
    queue_id: str, new_info: schemas.QueueUpdate, db: Session = Depends(get_db)
):
    db_queue = crud.read_queue_by_id(db, queue_id)
    if not db_queue:
        raise HTTPException(
            status_code=404, detail=f"Queue with the id='{queue_id}' is not found"
        )

    return crud.update_queue(db, db_queue, new_info)


@router.delete("/{queue_id}")
async def remove_queue(queue_id: str, db: Session = Depends(get_db)):
    db_queue = crud.read_queue_by_id(db, queue_id)
    if not db_queue:
        raise HTTPException(
            status_code=404, detail=f"Queue with id='{db_queue}' is not found"
        )

    crud.delete_queue(db, db_queue)

    return JSONResponse(status_code=204)
