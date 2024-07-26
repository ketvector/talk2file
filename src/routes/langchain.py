from fastapi import APIRouter, Query, HTTPException
from typing import Annotated


from ..langchain.service import add_file_to_store, query as query_service
from ..slack.service import send
from ..schemas.langchain import QueryAndPostBody
from ..schemas.common import AddToStoreBody
import os
import json


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

#TODO: Generalise to targets other than slack
@router.post("/query")
async def queryAndPost(body: QueryAndPostBody):
    answer = query_service(store_ids=body.storeids, questions=body.questions)
    send_to  = body.sendto[0]
    if send_to.target == "slack":
        send(json.dumps(answer, indent=4), send_to.channel, send_to.username, os.environ['SLACK_WORKSPACE_ACCESS_TOKEN'])
        return {
            "answer" : answer,
            "sendto" : [{
                "target" : "slack",
                "status": "success"
            }]
        }
    else:
        HTTPException(400, detail="Invalid target type")
    
    