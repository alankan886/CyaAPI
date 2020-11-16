from sqlalchemy.orm import Session

from .. import models
from .. schemas import Board, BoardCreate


def get_board_by_id(db: Session, board_id: int):
    return db.query(models.Board).filter(models.Board.id == board_id).first()


def get_board_by_name(db: Session, board_name: str):
    return db.query(models.Board).filter(models.Board.name == board_name).first()


def get_boards(db: Session):
    return db.query(models.Board).all()


def create_board(db: Session, board: BoardCreate):
    db_board = models.Board(name=board.name)
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    return db_board


def remove_board(db: Session, board: Board):
    db.delete(board)
    db.commit()
