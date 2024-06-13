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

"""
/signup
method: POST
header: {
    id: str,
    pw: str
}

response: {
    status: int,
    message: str
}
"""

"""
/signin
method: GET
header: {
    id: str,
    pw: str
}

response: {
    status: int,
    message: str
}
"""


"""
/check
method: GET
header: {
    id: str,
    pw: str
}

response: {
    status: int,
    message: str
}
"""

"""
/post
method: POST
header: {
    id: str,
    pw: str,
    title: str,
    content: str
}

response: {
    status: int,
    message: str
}
"""


"""
/post
method: GET
header: {
    page: int = 0
}

response: {
    status: int,
    posts: [
        {
            title: str,
            content: str,
            writer: str,
            id: str
        }, ...
    ],
    message: str,
    next: int
}
"""


"""
/post
method: DELETE
header: {
    id: str,
    pw: str,
    post_id: str
}

response: {
    status: int,
    message: str
}
"""