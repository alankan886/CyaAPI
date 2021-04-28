from fastapi import FastAPI
from .routers import stack, card

from . import crud, schemas

app = FastAPI(title="CYA API")

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
