from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..utils.auth_helper import get_current_user
from typing import Optional
from urllib.parse import quote_plus

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/", response_model=schemas.CommentOut, status_code=status.HTTP_201_CREATED)
def create_comment(
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Create a new comment on a blog post.
    
    Validation:
    - Requires authentication via JWT token (get_current_user dependency)
    - user_id is automatically extracted from authenticated session
    - post_id is required in request body and must exist
    - content is required and validated by CommentCreate schema
    """
    # Validate post exists
    post = db.query(models.Post).get(comment.post_id)
    if not post:
        raise HTTPException(
            status_code=404, 
            detail=f"Post with ID {comment.post_id} not found. Cannot create comment."
        )

    db_comment = models.Comment(
        content=comment.content,
        post_id=comment.post_id,
        user_id=current_user.id,
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)

    # Build author info for response
    author_name = current_user.name
    avatar = (
        f"https://ui-avatars.com/api/?name={quote_plus(author_name)}&background=ddd&color=555&rounded=true"
        if author_name
        else None
    )

    return {
        "id": db_comment.id,
        "content": db_comment.content,
        "post_id": db_comment.post_id,
        "user_id": db_comment.user_id,
        "created_at": db_comment.created_at,
        "author_name": author_name,
        "author_avatar": avatar,
    }


@router.get("/post/{post_id}", response_model=List[schemas.CommentOut])
def list_comments_for_post(post_id: int, db: Session = Depends(get_db)):
    # join comments with users to fetch author name in a single query
    rows = (
        db.query(models.Comment, models.User.name)
        .join(models.User, models.User.id == models.Comment.user_id)
        .filter(models.Comment.post_id == post_id)
        .order_by(models.Comment.created_at.desc())
        .all()
    )

    out = []
    for c, author_name in rows:
        avatar = (
            f"https://ui-avatars.com/api/?name={quote_plus(author_name)}&background=ddd&color=555&rounded=true"
            if author_name
            else None
        )
        out.append(
            {
                "id": c.id,
                "content": c.content,
                "post_id": c.post_id,
                "user_id": c.user_id,
                "created_at": c.created_at,
                "author_name": author_name,
                "author_avatar": avatar,
            }
        )
    return out


@router.put("/{comment_id}", response_model=schemas.CommentOut)
def update_comment(
    comment_id: int,
    payload: schemas.CommentUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    comment = db.query(models.Comment).get(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    # Only the author or admin can edit
    if comment.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    if payload.content is not None:
        comment.content = payload.content

    db.commit()
    db.refresh(comment)

    # fetch author name from users table
    user = db.query(models.User).filter(models.User.id == comment.user_id).first()
    author_name = user.name if user else None
    avatar = (
        f"https://ui-avatars.com/api/?name={quote_plus(author_name)}&background=ddd&color=555&rounded=true"
        if author_name
        else None
    )

    return {
        "id": comment.id,
        "content": comment.content,
        "post_id": comment.post_id,
        "user_id": comment.user_id,
        "created_at": comment.created_at,
        "author_name": author_name,
        "author_avatar": avatar,
    }


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Delete a comment.
    
    Validation:
    - Requires authentication via JWT token (get_current_user dependency)
    - Requires comment_id in URL path
    - User must be the comment author OR have admin role
    """
    # Validate comment exists
    comment = db.query(models.Comment).get(comment_id)
    if not comment:
        raise HTTPException(
            status_code=404, 
            detail=f"Comment with ID {comment_id} not found"
        )

    # Validate ownership: only author or admin can delete
    if comment.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=403, 
            detail=f"Not authorized to delete this comment. User ID {current_user.id} does not own comment ID {comment_id}"
        )

    db.delete(comment)
    db.commit()
    return None
