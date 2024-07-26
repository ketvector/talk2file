from fastapi import APIRouter, Query
from typing import Annotated

import os

from ..openai_assistants.service import query as query_service, add_file_to_store, create_agent as create_agent_service, create_store as create_store_service
from ..schemas.common import AddToStoreBody, CreateAgent, CreateStore

router = APIRouter(
    prefix="/oaiasst",
    tags=["open-ai-assistant"]
)

@router.post("/store")
async def create_store(body: CreateStore):
    id = create_store_service(body.name).get_id()
    return {
        "id": id
    }

@router.post("/store/add")
async def add_to_store(body: AddToStoreBody):
    # TODO: better error handling
    file_path = os.environ['LOCAL_FILE_UPLOAD_DIRECTORY']
    add_file_to_store(body.store_id, f"{file_path}/{body.file_id}.pdf")
    return {
        "status" : "success"
    }

@router.get("/query")
async def query(agentid: str, storeids: Annotated[list[str] | None, Query()],  questions: Annotated[list[str] | None, Query()]):
    answer = query_service(agent_id=agentid, store_ids=storeids, questions=questions)
    print(answer)
    return answer

@router.post("/agent")
async def create_agent(body: CreateAgent):
    id = create_agent_service(body.name).get_id()
    return {
        "status" : "success",
        "id" : id
    }


    
