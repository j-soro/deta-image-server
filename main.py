import os

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse
from deta import Deta
from dotenv import load_dotenv

load_dotenv()
PROJECT_KEY = os.environ['project_key']

app = FastAPI()
deta = Deta(PROJECT_KEY) # configure your deta project
drive = deta.Drive("images") # access to your drive


# get all images
@app.get("/", response_class=HTMLResponse)
def render():
    return """
    <form action="/upload" enctype="multipart/form-data" method="post">
        <input name="file" type="file">
        <input type="submit">
    </form>
    """


# upload images
@app.post("/upload")
def upload_img(file: UploadFile = File(...)):
    name = file.filename
    f = file.file
    res = drive.put(name, f)
    return res


# download images
@app.get("/download/{name}")
def download_img(name:str):
    res = drive.get(name)
    return StreamingResponse(res.iter_chunks(1024), media_type="image/png")
