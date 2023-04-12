from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

import src.oauth2 as oauth2
from src import models
from src.database import get_db
from src.schemas import Vote

router = APIRouter(
    prefix="/api/v1/votes",
    tags=["Votes resources"],
)


@router.post("", response_model=dict[str, str], status_code=status.HTTP_201_CREATED)
def vote(request: Vote, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == request.post_id,
                                              models.Vote.user_id == current_user.id)

    if request.direction == 1:
        if vote_query.first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with id: {current_user.id} already voted for post with id: {request.post_id}!")

        if not db.query(models.Post).filter(models.Post.id == request.post_id).first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id: {request.post_id} not found!")

        new_vote = models.Vote(post_id=request.post_id, user_id=current_user.id)

        db.add(new_vote)
        db.commit()

        return {"message": f"Vote added to post with id {request.post_id} successfully!"}

    else:
        if not vote_query.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id: {current_user.id} already voted for post with id: {request.post_id}!")

        vote_query.delete(syncronize_session=False)
        db.commit()

        return {"message": f"Vote removed from post with id {request.post_id} successfully!"}
