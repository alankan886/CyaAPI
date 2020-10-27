from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..extensions.db import get_db


router = APIRouter()


@router.get('/{board_id}', response_model=schemas.Board)
def read_board(board_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_board(db, board_id=board_id)
    if not db_user:
        raise HTTPException(status_code=404, detail='Board not found')
    return db_user


@router.get('/')
def read_all_boards():
    return {'all boards'}


@router.post('/')
def create_board(board: schemas.Board):
    return {'Hello': 'Cards'}


@router.put('/{board_id}')
def update_board(board: schemas.Board, card_id: int):
    return {'Hello': 'Cards'}


@router.delete('/{board_id}')
def delete_board(board_id: int):
    return {'Hello': 'Cards'}
