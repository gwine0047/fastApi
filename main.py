from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title :str
    content: str
    published: bool = True
    rating: Optional [int] = None

my_posts = [{"title": "title1", "content": "content1", "id" : 1}, {"title": "favourite foods", "content" : "i like pizza", "id" : 2}]

@app.get("/")
async def root():
  return {"message": "Hello Godwin and Abimbola"}


def find_post(id):
    for post in my_posts:
       if post["id"] == id:
          return post

def find_index_post(id):
    for i, post in enumerate(my_posts):
       if post["id"] == id:
          return i

@app.get("/posts")
def get_posts():
  return {"This is your post\n": my_posts}  


@app.post("/posts", status_code=status.HTTP_201_CREATED)
# it will extract all the fields, convert it into a python dict and store it in payload
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/post/{id}")
def get_post(id: int):
   post = find_post(id)
   print(id)
   if not post:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"post with {id} was not found")
    #   response.status_code = status.HTTP_404_NOT_FOUND
    #   return{'message': f"Post with {id} was nit found"}
   return {"post details" : post}


@app.delete("/posts/{id}")
def delete_posts(id: int):
    index = find_index_post(id)
    print(index)

    my_posts.pop(index)
    return{"Message" : f"Post with id {id}  and at index {index} was successfully deleted"}
