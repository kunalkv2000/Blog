from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..utils.auth_helper import get_current_user

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Create a new blog post.
    
    Validation:
    - Requires authentication via JWT token (get_current_user dependency)
    - user_id is automatically extracted from authenticated session
    - title and content are required fields validated by PostCreate schema
    """
    db_post = models.Post(
        title=post.title,
        content=post.content,
        owner_id=current_user.id,  # user_id from authenticated session
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.get("/", response_model=List[schemas.Post])
def list_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).all()


@router.get("/{post_id}", response_model=schemas.Post)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.put("/{post_id}", response_model=schemas.Post)
def update_post(
    post_id: int,
    post_update: schemas.PostUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    post = db.query(models.Post).get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # authorization: owner or admin
    if not (current_user.role == "admin" or current_user.id == post.owner_id):
        raise HTTPException(status_code=403, detail="Not authorized to update this post")

    post.title = post_update.title
    post.content = post_update.content
    db.commit()
    db.refresh(post)
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Delete a blog post.
    
    Validation:
    - Requires authentication via JWT token (get_current_user dependency)
    - Requires post_id in URL path
    - User must be the post owner OR have admin role
    """
    # Validate post exists
    post = db.query(models.Post).get(post_id)
    if not post:
        raise HTTPException(
            status_code=404, 
            detail=f"Post with ID {post_id} not found"
        )
    
    # Validate ownership: only owner or admin can delete
    if not (current_user.role == "admin" or current_user.id == post.owner_id):
        raise HTTPException(
            status_code=403, 
            detail=f"Not authorized to delete this post. User ID {current_user.id} does not own post ID {post_id}"
        )

    db.delete(post)
    db.commit()
    return None
