from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..extensions.db import get_db

router = APIRouter()

boards_responses = {
    404: {
        "description": "Boards not found",
        "content": {
            "application/json": {
                "example": {"detail": "No boards are found"}
            }
        }
    }
}

board_responses = {
    404: {
        "description": "Board not found",
        "content": {
            "application/json": {
                "example": {"detail": "Board is not found"}
            }
        }
    }
}


@router.get('/{board_id}', response_model=schemas.Board, responses={**board_responses})
def read_board(board_id: int, db: Session = Depends(get_db)):
    db_board = crud.get_board_by_id(db, board_id=board_id)
    if not db_board:
        raise HTTPException(status_code=404, detail=f'Board with id={board_id} not found')
    return db_board


@router.get(
    "",
    response_model=List[schemas.Board],
    responses={**boards_responses}
)
def read_all_boards(db: Session = Depends(get_db)):
    db_boards = crud.get_boards(db)
    if not db_boards:
        raise HTTPException(status_code=404, detail="No boards are found")
    return db_boards


# "" path because the prefix is /boards, then with redirect slashes, that makes the path /boards/
@router.post(
    "",
    response_model=schemas.Board,
    responses={
        400: {
            "description": "Board with the name has already exists",
            "content": {
                "application/json": {
                    "example": {"detail": "Board with the name Board1 has already exists"}
                }
            }
        }
    })
def create_board(board: schemas.BoardCreate, db: Session = Depends(get_db)):
    db_board = crud.get_board_by_name(db, board_name=board.name)
    if db_board:
        raise HTTPException(status_code=400, detail=f"Board with the name {board.name} has already exists")
    return crud.create_board(db=db, board=board)


@router.delete('/{board_id}', response_model=schemas.Board, responses={**board_responses})
def delete_board(board_id: int, db: Session = Depends(get_db)):
    db_board = crud.get_board_by_id(db, board_id=board_id)
    if not db_board:
        raise HTTPException(status_code=404, detail=f"Board with id={board_id} is not found")
    crud.delete_board(db, db_board)
    return db_board
