from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    id: Optional[int]=None
    title: str
    content: str
    pages: int

my_posts = [{"id":1,"title": "First Post", "content": "This is the content of the first post", "pages": 100},
            {"id":2,"title": "Second Post", "content": "This is the content of the second post", "pages": 200}]

"""Define a root ("/") endpoint """
@app.get("/")
def root_path():
    return "This is The root path  of APi"

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts")
def create_post(input_post:Post):
    input_post_dict = input_post.dict()
    input_post_dict['id']= len(my_posts) + 1
    my_posts.append(input_post_dict)
    return {"New Created Post": input_post_dict}


@app.get("/posts/latest")
def get_latest_post():
    latest_post = my_posts[-1]
    return {"Latest Post": latest_post}


@app.get("/posts/{input_id}")
def get_post_by_id (input_id :int):
    result = None
    print("Searching For post Id :", input_id)
    for post in my_posts:
        print(f"Input Post id :{input_id} type : {type(input_id)}  post id :{post['id']} post id type :{type(post['id'])}")
        if post['id']==input_id:
            result = post
    if result:
        return {"Post": post}
    else:
        return {"Error Message":f"Could not find any post with id :{input_id}"}
    

@app.get("/posts/get/latest")
def get_latest_post():
    latest_post = my_posts[-1]
    return {"Latest Post": latest_post}