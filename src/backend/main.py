from fastapi import FastAPI, File, UploadFile
from PIL import Image
import aiofiles
import base64
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/database/{filename}")
async def get_image(filename: str):
    return FileResponse(f"database/{filename}")

@app.post("/queryImage")
async def upload_file(imageFile: UploadFile):
    out_path = f"database/temp"
    with open(out_path, "wb") as f:
        contents = imageFile.file.read()
        f.write(contents)
    imageFile.file.close()
    return {"status": "ok"}