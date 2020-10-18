from fastapi import APIRouter

from .. models import Board


router = APIRouter()


@router.get('/{board_id}')
def read_board(board_id: int):
    return {'Hello': 'Cards'}


@router.get('/')
def read_all_boards():
    return {'all boards'}


@router.post('/')
def create_board(board: Board):
    return {'Hello': 'Cards'}


@router.put('/{board_id}')
def update_board(board: Board, card_id: int):
    return {'Hello': 'Cards'}


@router.delete('/{board_id}')
def delete_board(board_id: int):
    return {'Hello': 'Cards'}
