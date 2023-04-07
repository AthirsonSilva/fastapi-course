import uuid


def convert_uuid_to_string(posts):
		return [{**post, "id": str(post["id"])} if isinstance(post["id"], uuid.UUID) else post for post in posts]