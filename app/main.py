from fastapi import FastAPI
from .routers import stack, card, card_details

from . import crud, schemas
from .db import SessionLocal, engine, Base

# models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="CYA API")

# cheange board to deck
app.include_router(
    stack.router,
    prefix='/stacks',
    tags=['stacks']
)

app.include_router(
    card.router,
    prefix='/cards',
    tags=['cards']
)

# app.include_router(
#     card_details.router,
#     prefix='/card_details',
#     tags=['card_details']
# )
