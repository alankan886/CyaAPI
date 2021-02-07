from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..db import get_db

router = APIRouter()

stacks_responses = {
    404: {
        "description": "Stacks not found",
        "content": {
            "application/json": {
                "example": {"detail": "No stacks are found"}
            }
        }
    }
}

stack_responses = {
    404: {
        "description": "Stack not found",
        "content": {
            "application/json": {
                "example": {"detail": "Stack is not found"}
            }
        }
    }
}


@router.get("/{stack_id}", response_model=schemas.Stack, responses={**stack_responses})
def get_stack(stack_id: int, db: Session = Depends(get_db)):
    db_stack = crud.read_stack_by_id(db, stack_id=stack_id)
    if not db_stack:
        raise HTTPException(status_code=404, detail=f'Stack with id={stack_id} not found')
    return db_stack


@router.get(
    "",
    response_model=List[schemas.Stack],
    responses={**stacks_responses}
)
def get_stacks(db: Session = Depends(get_db)):
    db_stacks = crud.read_stacks(db)
    if not db_stacks:
        return []
    return db_stacks


@router.get("/{stack_id}/cards")
def get_cards_in_stack(stack_id: int, db: Session = Depends(get_db)):
    cards = crud.read_cards_in_stacks(db, stack_id)
    return cards


# "" path because the prefix is /stacks, then with redirect slashes, that makes the path /stacks/
@router.post(
    "",
    response_model=schemas.Stack,
    responses={
        400: {
            "description": "Board with the name has already exists",
            "content": {
                "application/json": {
                    "example": {"detail": "Board with the name Board1 has already exists"}
                }
            }
        }
    },
    status_code=201
)
def post_stack(stack: schemas.StackCreate, db: Session = Depends(get_db)):
    db_stack = crud.read_stack_by_name(db, stack_name=stack.name)
    if db_stack:
        raise HTTPException(status_code=400, detail=f"Stack with the name {stack.name} has already exists")
    return crud.create_stack(db=db, stack=stack)


@router.put("/{stack_id}", response_model=schemas.Stack)
def update_stack(stack_id: int, new_info: schemas.StackCreate, db: Session = Depends(get_db)):
    db_stack = crud.read_stack_by_id(db, stack_id=stack_id)
    if not db_stack:
        stack = crud.create_stack(db, stack=new_info)
        return JSONResponse(status_code=201, content=stack)
    return crud.update_stack(db, stack=db_stack, new_info=new_info)


@router.delete("/{stack_id}", response_model=schemas.Stack, responses={**stack_responses})
def delete_stack(stack_id: int, db: Session = Depends(get_db)):
    db_stack = crud.read_stack_by_id(db, stack_id=stack_id)
    if not db_stack:
        raise HTTPException(status_code=404, detail=f"Stack with id={stack_id} is not found")
    crud.delete_stack(db, db_stack)
    return JSONResponse(status_code=204)
