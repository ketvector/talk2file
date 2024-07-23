from fastapi import FastAPI

from .routes import oaiasst

app = FastAPI()

app.include_router(oaiasst.router)

@app.get("/")
async def root():
    return {"message" : "Hello !"}