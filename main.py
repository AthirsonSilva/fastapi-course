import uuid
from fastapi import FastAPI, status, HTTPException
from fastapi.responses import JSONResponse
from Post import Post
from posts import posts
from utils import convert_uuid_to_string

app = FastAPI()


@app.get("/")
async def root() -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Welcome to my blog!"})

@app.post("/api/v1/posts")
async def create(request: Post) -> JSONResponse:
    post_dict = request.dict()
    post_dict["id"] = uuid.uuid4()
    posts.append(post_dict)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Post created successfully!", "data": post_dict})


@app.get("/api/v1/posts/latest")
async def find_latest() -> JSONResponse:
    post = posts[-1]

    if not post:
        raise HTTPException(
            status_code=404, detail=f"Post with id: {id} not found!")

    return JSONResponse(status_code=status.HTTP_200_OK, content={"data": convert_uuid_to_string([post])})


@app.get("/api/v1/posts")
async def find_all() -> JSONResponse:
	return JSONResponse(status_code=status.HTTP_200_OK, content={"data": convert_uuid_to_string(posts)})


@app.get("/api/v1/posts/{id}")
async def find_one(id: str) -> JSONResponse:
    try:
        post = [post for post in posts if post["id"] == id]

        if not post:
            raise HTTPException(
                status_code=404, detail=f"Post with id: {id} not found!")

        return JSONResponse(status_code=status.HTTP_200_OK, content={"data": post})

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format!")


@app.delete("/api/v1/posts/{id}")
async def delete(id: str) -> JSONResponse:
    try:
        post = [post for post in posts if post["id"] == id]

        if not post:
            raise HTTPException(
                status_code=404, detail=f"Post with id: {id} not found!")

        posts.remove(post[0])

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format!")

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"message": "Post deleted successfully!"})


@app.put("/api/v1/posts/{id}")
async def update(id: str, request: Post) -> JSONResponse:
    try:
        for index, post in enumerate(posts):
            if post["id"] == id:
                posts[index] = request.dict()
                posts[index]["id"] = id

                return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Post updated successfully!", "data": posts[index]})

        raise HTTPException(
            status_code=404, detail=f"Post with id: {id} not found!")

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format!")
