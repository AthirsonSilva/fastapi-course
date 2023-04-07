import uuid
from fastapi import FastAPI, Response, status, Body, HTTPException
from Post import Post
from posts import posts

app = FastAPI()


@app.get("/")
async def root() -> Response:
    return Response(status_code=status.HTTP_200_OK, content=Body({"message": "Welcome to my blog!"}))


@app.post("/api/v1/posts")
async def create(request: Post) -> Response:
    post_dict = request.dict()
    post_dict["id"] = uuid.uuid4()
    posts.append(post_dict)

    return Response(status_code=status.HTTP_201_CREATED, content=Body({"message": "Post created successfully!", "data": post_dict}))


@app.get("/api/v1/posts/latest")
async def find_latest() -> Response:
    post = posts[-1]

    if not post:
        raise HTTPException(status_code=404, detail="Post not found!")

    return Response(status_code=status.HTTP_200_OK, content=Body({"data": post}))


@app.get("/api/v1/posts")
async def find_all() -> Response:
    return Response(status_code=status.HTTP_200_OK, content=Body({"data": posts}))


@app.get("/api/v1/posts/{id}")
async def find_one(id: str) -> Response:
    try:
        post = [post for post in posts if post["id"] == id]

        if not post:
            raise HTTPException(status_code=404, detail="Post not found!")
        
        return Response(status_code=status.HTTP_200_OK, content=Body({"data": post}))

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format!")


@app.delete("/api/v1/posts/{id}")
async def delete(id: str) -> Response:
    try:
        post = [post for post in posts if post["id"] == id]

        if not post:
            raise HTTPException(status_code=404, detail="Post not found!")

        posts.remove(post[0])

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format!")

    return Response(status_code=status.HTTP_204_NO_CONTENT, content=Body({"message": "Post deleted successfully!"}))


@app.put("/api/v1/posts/{id}")
async def update(id: str, request: Post) -> Response:
    try:
        for index, post in enumerate(posts):
            if post["id"] == id:
                posts[index] = request.dict()
                posts[index]["id"] = id

                return Response(status_code=status.HTTP_202_ACCEPTED, content=Body({"message": "Post updated successfully!", "data": posts[index]}))

        raise HTTPException(status_code=404, detail="Post not found!")

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format!")
