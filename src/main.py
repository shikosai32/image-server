import os
from typing import Optional
from fastapi import FastAPI, File, UploadFile, Header
from fastapi.responses import HTMLResponse, StreamingResponse
from deta import Deta
from dotenv import load_dotenv

load_dotenv()

PROJECT_KEY = os.environ["PROJECT_KEY"]
DRIVE_NAME = os.environ["DRIVE_NAME"]
TOKEN = os.environ["TOKEN"]

app = FastAPI()
deta = Deta(PROJECT_KEY)
drive = deta.Drive(DRIVE_NAME)

@app.get("/")
def root():
    return "Hi"

@app.get("/{name}")
def get_img(name: str):
    res = drive.get(name)
    if res:
        return StreamingResponse(res.iter_chunks(1024), media_type="image/png")
    else:
        return f"Not Found {name}.png"

@app.post("/{name}")
def upload_img(name: str, file: UploadFile = File(...), token: Optional[str] = Header(None)):
    if token == TOKEN:
        f = file.file
        res = drive.put(name, f)
        return res
    else:
        return "Invalid TOKEN"

@app.delete("/{name}")
def delete_img(name: str, token: Optional[str] = Header(None)):
    if token == TOKEN:
        res = drive.delete(name)
        return res
    else:
        return "Invalid TOKEN"
