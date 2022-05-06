from fastapi import FastAPI
from .routers import queues, items

app = FastAPI()

app.include_router(queues.router)
app.include_router(items.router)