from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import Annotated


from ..langchain.service import add_file_to_store, query as query_service

class AddToStoreBody(BaseModel):
    store_id: str
    file_path: str

router = APIRouter(
    prefix="/langchain",
    tags=["langchain"]
)

@router.post("/store/add")
async def add_to_store(body: AddToStoreBody):
    add_file_to_store(body.store_id, body.file_path)
    return {
        "status" : "success"
    }

#TODO: Add agentId support
@router.get("/query")
async def query(storeids: Annotated[list[str] | None, Query()],  questions: Annotated[list[str] | None, Query()]):
    answer = query_service(store_ids=storeids, questions=questions)
    print(answer)
    return answer
    