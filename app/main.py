from fastapi import FastAPI
from .routers import card, board

from . import crud, schemas
from .db import SessionLocal, engine, Base

# models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="CYA API")

app.include_router(
    board.router,
    prefix='/boards',
    tags=['boards']
)

app.include_router(
    card.router,
    prefix='/cards',
    tags=['cards']
)
