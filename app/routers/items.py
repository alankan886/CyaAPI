from fastapi import APIRouter

from ..schemas import Item

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}}
    )


@router.get("/", response_model = Item)
async def read_items():
    return {"hello": "world"}

@router.post("/")
async def create_item():
    return {"hello": "world"}

@router.put("/{item_id}")
async def update_item(item_id: str):
    return {"hello": "world"}

@router.delete("/{item_id}")
async def remove_item(item_id: str):
    return {"hello": "world"}