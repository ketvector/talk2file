from pydantic import BaseModel

class AddToStoreBody(BaseModel):
    store_id: str
    file_id: str