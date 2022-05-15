from fastapi import APIRouter

from app.api.endpoints import queues, items

api_router = APIRouter()
api_router.include_router(queues.router, prefix="/queues", tags=["Queues"])
api_router.include_router(items.router, prefix="/items", tags=["Items"])
