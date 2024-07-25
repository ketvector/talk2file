from fastapi import FastAPI

from dotenv import load_dotenv

from .routes import oaiasst, langchain, file

load_dotenv(override=True)

app = FastAPI()
app.include_router(oaiasst.router)
app.include_router(langchain.router)
app.include_router(file.router)

@app.get("/")
async def root():
    return {"message" : "Hello !"}