from fastapi import APIRouter

router = APIRouter(
    prefix="/queues",
    tags=["queues"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_queues():
    # TODO: add pagination?
    return {"hello": "world"}

@router.post("/")
async def create_queue():
    return {"hello": "world"}

@router.put("/{queue_id}")
async def update_queue(queue_id: str):
    return {"hello": "world"}

@router.delete("/{queue_id}")
async def remove_queue(queue_id: str):
    return {"hello": "world"}