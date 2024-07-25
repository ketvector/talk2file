from fastapi import APIRouter, Query
from typing import Annotated

import os

from ..openai_assistants.service import query as query_service, add_file_to_store
from ..schemas.common import AddToStoreBody

router = APIRouter(
    prefix="/oaiasst",
    tags=["open-ai-assistant"]
)
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
    
    
