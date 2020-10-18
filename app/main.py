from fastapi import FastAPI
from . routers import cards, boards


app = FastAPI(title="CYA API")


app.include_router(
    boards.router,
    prefix='/boards',
    tags=['boards']
)

app.include_router(
    cards.router,
    prefix='/cards',
    tags=['cards']
)
