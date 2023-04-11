from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

import base64
import h5py
import cv2
import numpy as np
from src.vlad import vlad
from src.utils import get_topk_indices

app = FastAPI()

model = vlad('output/cluster.joblib')
with h5py.File('output/vlads.h5', 'r') as f:
    db_vlad = f['vlads'][:]
    db_names = f['names'][:]
    db_names = [name.decode('utf-8') for name in db_names]

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
    
    results = []
    indices = get_topk_indices(db_vlad, model.calculate_VLAD(image), 5)
    indices = indices[0]
    for i in indices:
        filename = db_names[i]
        with open(f"{filename}", "rb") as f:
            image_data = f.read()
            base64_encoded_data = base64.b64encode(image_data).decode('utf-8')
            results.append(
                {
                    "name": filename,
                    "image": base64_encoded_data
                }
            )

    return {"status": "ok", "results" : results}