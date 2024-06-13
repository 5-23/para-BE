from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# public폴더를 static으로
app.mount("/public", StaticFiles(directory="public"), name="public")

# index.html 반환
@app.get("/", response_class=HTMLResponse)
def read_root():
    return FileResponse("./public/index.html")  

# @app.