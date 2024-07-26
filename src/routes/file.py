import aiofiles
from fastapi import APIRouter, UploadFile, HTTPException
import os

router = APIRouter(
    prefix="/file",
    tags=["file"]
)

@router.post("/upload/")
async def create_upload_file(file: UploadFile, id: str):
    #TODO: Validate the input file is pdf https://github.com/tiangolo/fastapi/issues/3364
    outpath_file = f"{os.environ['LOCAL_FILE_UPLOAD_DIRECTORY']}/{id}.pdf"
    async with aiofiles.open(outpath_file, 'wb+') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write

    return {"in_filename": file.filename , "id": id, "result": "OK"}