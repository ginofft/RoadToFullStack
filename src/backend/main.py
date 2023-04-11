from fastapi import FastAPI, File, UploadFile
from PIL import Image
import aiofiles
import base64
import cv2
import numpy as np
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
    image = cv2.imdecode(np.frombuffer(imageFile.file.read(),dtype = np.uint8), cv2.IMREAD_COLOR)
    cv2.imwrite("database/1.jpg", image) 
    return {"status": "ok"}
