import uuid
from fastapi import FastAPI
from Post import Post
from posts import posts

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/api/v1/posts")
async def create(request: Post):
    post_dict = request.dict()
    post_dict["id"] = uuid.uuid4()
    posts.append(post_dict)

    return {"message": "Post created successfully!", "data": post_dict}


@app.get("/api/v1/posts/latest")
async def find_latest() -> dict[str, str | dict]:
    post = posts[-1]

    if not post:
        return {"message": "Post not found!"}

    return {"data": post}


@app.get("/api/v1/posts")
async def find_all() -> dict[str, list[dict]]:
    return {"data": posts}


@app.get("/api/v1/posts/{id}")
async def find_one(id: str) -> dict[str, str | list[dict]]:
    try:
        post = [post for post in posts if post["id"] == id]

        if not post:
            return {"message": "Post not found!"}

    except ValueError:
        return {"message": "Invalid ID format!"}

    return {"data": post}


@app.delete("/api/v1/posts/{id}")
async def delete(id: str) -> dict[str, str]:
    try:
        post = [post for post in posts if post["id"] == id]

        if not post:
            return {"message": "Post not found!"}

        posts.remove(post[0])

    except ValueError:
        return {"message": "Invalid ID format!"}

    return {"message": "Post deleted successfully!"}


@app.put("/api/v1/posts/{id}")
async def update(id: str, request: Post) -> dict[str, str | dict]:
    try:
        for index, post in enumerate(posts):
            if post["id"] == id:
                posts[index] = request.dict()
                posts[index]["id"] = id

                return {"message": "Post updated successfully!", "data": posts[index]}

        return {"message": "Post not found!"}

    except ValueError:
        return {"message": "Invalid ID format!"}
