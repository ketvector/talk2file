from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import Annotated


from ..langchain.service import add_file_to_store, query as query_service
import os
class AddToStoreBody(BaseModel):
    store_id: str
    file_id: str

router = APIRouter(
    prefix="/langchain",
    tags=["langchain"]
)

@router.post("/store/add")
async def add_to_store(body: AddToStoreBody):
    file_path = os.environ['LOCAL_FILE_UPLOAD_DIRECTORY']
    add_file_to_store(body.store_id, f"{file_path}/{body.file_id}.pdf")
    return {
        "status" : "success"
    }

#TODO: Add agentId support
@router.get("/query")
async def query(storeids: Annotated[list[str] | None, Query()],  questions: Annotated[list[str] | None, Query()]):
    answer = query_service(store_ids=storeids, questions=questions)
    print(answer)
    return answer
    