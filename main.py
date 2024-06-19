from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from typing import Annotated
from env import MONGODB_URI
# load_dotenv()

import os
import json
from pymongo import MongoClient
from bson.json_util import dumps

client = MongoClient(MONGODB_URI)
db = client["ny64"]
print("Database connected!")

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
    passwd: str
}

response: {
    status: int,
    message: str
}
"""
@app.post("/signup")
def signup(id: str = Header(None), passwd: str = Header(None)):
    # id, pw가 None인 경우 400 에러 반환
    if id is None or passwd is None:
        raise HTTPException(status_code=400, detail="id or pw is None")
    
    # 입력한 id가 이미 db에 있다면 400 에러 반환
    if db['users'].find_one({"id": id}):
        raise HTTPException(status_code=400, detail="id already exists")
        
    # db에 사용자 추가
    db['users'].insert_one({"id": id, "pw": passwd})
    
    return {'status': 200, 'message': 'success'}
    

"""
/signin
method: GET
header: {
    id: str,
    passwd: str
}

response: {
    status: int,
    message: str
}
"""




@app.post("/signin")
def signin(id: str = Header(None), passwd: str = Header(None)):
    if id is None or passwd is None:
        raise HTTPException(status_code=400, detail="id or pw is None")

    if db['users'].find_one({"id": id, "pw": passwd}):
        return {'status': 200, 'message': 'success'}
    else:
        raise HTTPException(status_code=400, detail="id or pw is wrong")










"""
/check
method: GET
header: {
    id: str,
    passwd: str
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
    passwd: str,
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
    passwd: str,
    post_id: str
}

response: {
    status: int,
    message: str
}
"""
