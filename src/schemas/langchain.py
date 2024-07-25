from pydantic import BaseModel

class AddToStoreBody(BaseModel):
    store_id: str
    file_id: str

class SendToSchema(BaseModel):
    target: str
    channel: str
    username: str

class QueryAndPostBody(BaseModel):
    questions: list[str]
    storeids: list[str]
    sendto: list[SendToSchema]