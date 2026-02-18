from typing import Any

from fastapi import APIRouter, HTTPException

from app.models.item import Item, Items

router = APIRouter()


@router.get("/", response_model=Items)
def read_items() -> Any:
    items = [Item(title="hoge", description="hoge"), Item(title="piyo", description="piyo")]
    print("debug items")

    return Items(data=items, count=2)
