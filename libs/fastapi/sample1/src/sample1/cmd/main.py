import time
from typing import Union

import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/")
async def root():
    results = await async_task()
    return results


async def async_task():
    time.sleep(5)
    return {"message": "Hello World"}


def debug():
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
