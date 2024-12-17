from enum import Enum
from typing import Annotated, Literal

import uvicorn
from fastapi import FastAPI, Query, Path
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str
    price: float
    description: str | None = None
    tax: float | None = None
    is_priceless : bool

class ModelName(str, Enum):
    alex = "alexbee"
    andriu = "andriubee"

class FilterParams(BaseModel):
    # If a client tries to send some extra data
    # in the query parameters, they will receive an error response.
    model_config = {"extra":"forbid"}

    limit: int = Field(100,gt=0,lt=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


app = FastAPI()

fake_db = [{"item_name":"foo"}, {"item_name":"bar"}, {"item_name":"baz"}]


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/models/{model_name}")
async def root(model_name: ModelName):
    if model_name == ModelName.alex:
        return {"model_name": ModelName.alex, "message": "Hello ALEX"}
    if model_name == ModelName.andriu:
        return {"model_name": ModelName.andriu, "message": "Hello ANDRIU"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

@app.get("/items/}")
async def read_items(q: str = None):
    return {"items": q}

@app.get("/list1/")
async def read_list(skip: int = 0, limit: int | None = len(fake_db)):
    if skip == None:
        return {"message": "good job this is first example with none!"}
    return {"items": fake_db[skip:skip+limit]}


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

@app.put("/items/{item_id}")
async def update_item(item_id: Annotated[str|None, Path(title="COOL")], item: Item = None):
    return {"item_id": item_id, **item.model_dump()}

@app.get("/items123/")
async def read_items_123(q : Annotated[str | None , Query(max_length=50,min_length=3 )] = None):
    return {"items": q}

@app.get("/items12/")
# we need to explicitly use Query, otherwise ot would be interpreted as a request body
async def read_items_12(q : Annotated[list[str] | None,
Query(description="thats cool!" ,alias="asd-1", deprecated=True, include_in_schema=False)] = ["foo","bar","baz"]):
    return {"items": q}


@app.get("/items3/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query

# workaround of the problem with the reloading and every time i need to kill the python process
# to get fully working app after stopping the server
# ----->
# This ensures that the port is freed and also terminates the program correctly.
if __name__ == "__main__":
    uvicorn.run("test_main:app", host="127.0.0.1", port=8000)