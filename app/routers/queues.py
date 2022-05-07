from fastapi import APIRouter

router = APIRouter(
    prefix="/queues",
    tags=["queues"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_queues():
    return {"queues": "world"}


@router.post("/")
async def create_queue():
    return {"queue_id": "world"}


@router.put("/{queue_id}")
async def update_queue(queue_id: str):
    return {"queue_id": "world"}


@router.delete("/{queue_id}")
async def remove_queue(queue_id: str):
    return {"queue_id": "world"}
