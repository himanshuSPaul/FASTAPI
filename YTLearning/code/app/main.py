from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
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

@app.post("/posts",status_code=status.HTTP_201_CREATED)
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
def get_post_by_id(input_id :int,response: Response):
    result = None
    print("Searching For post Id :", input_id)
    for post in my_posts:
        print(f"Input Post id :{input_id} type : {type(input_id)}  post id :{post['id']} post id type :{type(post['id'])}")
        if post['id']==input_id:
            result = post
    # Raise HTTP Exception If post not found
    if result:
        return {"Post": post}
    else :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Could not locate any post with id :{input_id}")
                     
    # Other way to handle above logic using HTTPException
    # if result:
    #     return {"Post": post}
    # else :
    #     response.status_code = status.HTTP_404_NOT_FOUND #404
    #     return {"Error Message":f"Could not locate any post with id :{input_id}"}
    

@app.get("/posts/get/latest")
def get_latest_post():
    latest_post = my_posts[-1]
    return {"Latest Post": latest_post}


@app.delete("/posts/{input_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post_by_id(input_id :int):
    """Search Index of post to be delelted """
    index_of_post_to_delete = None
    print("Searching For post Id to delete :", input_id)
    for index, post in enumerate(my_posts):
        print(f"Input Post id :{input_id} type : {type(input_id)}  post id :{post['id']} post id type :{type(post['id'])}")
        if post['id']==input_id:
            index_of_post_to_delete = index
            print(f"Found post id {input_id} at index :{index_of_post_to_delete}")
            
    """If index found then delete the post otherwise raise HTTP exception """
    if index_of_post_to_delete is not None:
            my_posts.pop(index_of_post_to_delete)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    else :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Could not locate any post with id :{input_id}")

@app.put("/posts/{input_id}")
def update_post_by_id(input_id: int, input_post:Post):
    """ Search index of post to be updated """
    index_of_post_to_be_delted =None 
    for index, post in enumerate(my_posts):
        if post['id']==input_id:
            index_of_post_to_be_delted = index

    if index_of_post_to_be_delted is not None:
        """ Convert Input Payload to dict """
        new_post_dict = input_post.dict()
        print("new_post_dict :", new_post_dict )
        """ Create dict with id and post payload"""
        new_post_dict['id']= input_id
        """ Update my_posts at found index with new dict"""
        my_posts[index_of_post_to_be_delted] = new_post_dict
        return f"Updated Post id :{input_id} with content :{new_post_dict}" 
    else :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Could not locate any post with id :{input_id}")