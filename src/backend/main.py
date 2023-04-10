from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/database/{filename}")
async def get_image(filename: str):
    return FileResponse(f"database/{filename}")

@app.post("/api/upload")
async def upload_file(image: UploadFile = File(...)):
    contents = await image.read()
    return {'status' : 'ok'}
