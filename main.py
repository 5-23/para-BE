from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from typing import Annotated
from env import MONGODB_URI
# load_dotenv()

import os
import json
from pymongo import MongoClient, DESCENDING
from bson.json_util import dumps
from bson import ObjectId
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
@app.get("/check")
def check(id: str = Header(None), passwd: str = Header(None)):
    if db['users'].find_one({"id": id, "pw": passwd}):
        return {'status': 200, 'message': 'success'}
    else:
        raise HTTPException(status_code=400, detail="id or pw is wrong")

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
@app.post("/post")
def create_post(id: str = Header(None), passwd: str = Header(None), title: str = Header(None), content: str = Header(None)):
    if id is None or passwd is None or title is None or content is None:
        raise HTTPException(status_code=400, detail="id, passwd, title or content is None")
    
    if not db['users'].find_one({"id": id, "pw": passwd}):
        raise HTTPException(status_code=400, detail="id or pw is wrong")
    
    db['posts'].insert_one({"author": id, "title": title, "content": content})
    return {'status': 200, 'message': 'Post created successfully'}

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
@app.get("/post")
def get_posts(page: int = Header(0)):
    posts_per_page = 5
    skip = page * posts_per_page
    cursor = db['posts'].find().sort("_id", DESCENDING).skip(skip).limit(posts_per_page)
    posts = [{"author": post["author"], "title": post["title"], "content": post["content"], "id": str(post["_id"])} for post in cursor]
    
    try:
        if (page+1)*5+1 > db['posts'].count_documents({}):
            return {'status': 200, 'posts': posts, 'message': 'success', 'next': None}
        return {'status': 200, 'posts': posts, 'message': 'success', 'next': page+1}
    except:
        return {'status': 200, 'posts': posts, 'message': 'success', 'next': None}

"""
/post
method: DELETE
header: {
    id: str,
    passwd: str,
    postid: str
}

response: {
    status: int,
    message: str
}
"""
@app.delete("/post")
def delete_post(id: str = Header(None), passwd: str = Header(None), postid: str = Header(None)):
    print(id, passwd, postid)
    # if id is None or passwd is None or postid is None:
    #     raise HTTPException(status_code=400, detail="id, passwd or post_id is None")
    if not db['users'].find_one({"id": id, "pw": passwd}):
        raise HTTPException(status_code=400, detail="id or pw is wrong")
    
    result = db['posts'].delete_one({"_id": ObjectId(postid), "author": id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Post not found or you are not the author")
    
    return {'status': 200, 'message': 'Post deleted successfully'}
