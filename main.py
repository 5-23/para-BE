from fastapi import FastAPI, Header
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from typing import Annotated
load_dotenv()

app = FastAPI()

# public폴더를 static으로
app.mount("/public", StaticFiles(directory="public"), name="public")

# index.html 반환
@app.get("/", response_class=HTMLResponse)
def read_root():
    return FileResponse("./public/index.html")  

@app.get("/post")
def get_post(
    page: Annotated[int, Header()] = 0
):
    posts = [
        {
            "author": "astara",
            "title": "nou1",
            "content": "str",
            "id": "1"
        },
        {
            "author": "asta",
            "title": "nou2",
            "content": "str",
            "id": "2"
        },
        {
            "author": "asta",
            "title": "nou3",
            "content": "str",
            "id": "3"
        },
        {
            "author": "asta",
            "title": "nou4",
            "content": "str",
            "id": "4"
        },
        {
            "author": "asta",
            "title": "nou5",
            "content": "str",
            "id": "5"
        },

        {
            "author": "asta",
            "title": "nou6",
            "content": "str",
            "id": "6"
        },

        {
            "author": "asta",
            "title": "nou7",
            "content": "str",
            "id": "7"
        },

        {
            "author": "asta",
            "title": "nou8",
            "content": "str",
            "id": "8"
        },
    ]
    if page*5+1 > posts.__len__():
        return {
            "status": 400,
            "message": "no more posts"
        }
    try:
        if (page+1)*5+1 > posts.__len__():
            return {
                "status": 200,
                "posts": posts[page*5:page*5+5],
                "message": "success",
                "next": None
            }
        return {
            "status": 200,
            "posts": posts[page*5:page*5+5],
            "message": "success",
            "next": page+1
        }
    except:
        return {
            "status": 200,
            "posts": posts[page*5:],
            "message": "success",
            "next": None
        }

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
            author: str,
            title: str,
            content: str,
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
