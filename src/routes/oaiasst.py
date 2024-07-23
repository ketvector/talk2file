from fastapi import APIRouter, Query
from typing import Annotated

from ..openai_assistants.service import query as query_service

router = APIRouter(
    prefix="/oaiasst",
    tags=["open-ai-assistant"]
)

@router.get("/query")
async def query(agentid: str, storeids: Annotated[list[str] | None, Query()],  questions: Annotated[list[str] | None, Query()]):
    answer = query_service(agent_id=agentid, store_ids=storeids, questions=questions)
    print(answer)
    return answer
    
    
