import os, glob
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import logging


logger_format = "%(levelname)s:     %(message)s"
logging.basicConfig(level=logging.DEBUG, format=logger_format)

logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

def get_photo_path(index):
    exts = ["jpg", "jpeg", "JPG", "JPEG","png"]
    for ext in exts:
        path1 = os.path.join("Photos", f"{index}.{ext}")
        if os.path.exists(path1):
            return path1
    return None

def get_data_file_path():
    path = os.path.join("Json", "info-*.json")
    
    files = glob.glob(path)
    files.sort(key=os.path.getmtime, reverse=True)
    if len(files) == 0:
        return None
    return files[0]

@app.get("/")
def root():
    return "Carriers Day 2024 - CV Book Data API"

@app.get("/data")
def data():
    path = get_data_file_path()
    if path is None:
        raise HTTPException(status_code=404, detail="Data file not found")
    else:
        path = os.path.abspath(path)
        return FileResponse(path)

@app.get("/photo/{index}")
def photo(index, q = None):
    path = get_photo_path(index)
    if path is None:
        path = get_photo_path("180XXX")
        return FileResponse(path)
    else:
        path = os.path.abspath(path)
        return FileResponse(path)
    
