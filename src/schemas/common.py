from pydantic import BaseModel

class AddToStoreBody(BaseModel):
    store_id: str
    file_id: str

class CreateAgent(BaseModel):
    name: str

class CreateStore(BaseModel):
    name: str