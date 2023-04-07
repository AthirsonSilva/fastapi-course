import uuid


posts = [
    {"id": "2ffb533c-3b2e-4bc6-a9c8-f41b7f9b8037", "title": "First post",
     "content": "This is my first post", "published": True, "rating": 5},
    {"id": uuid.uuid4(), "title": "Second post",
     "content": "This is my second post", "published": False, "rating": 4},
    {"id": uuid.uuid4(), "title": "Third post",
     "content": "This is my third post", "published": True, "rating": 3},
    {"id": uuid.uuid4(), "title": "Fourth post",
     "content": "This is my fourth post", "published": False, "rating": 2},
]
