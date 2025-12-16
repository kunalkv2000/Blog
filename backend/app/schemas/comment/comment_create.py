from typing import Optional
from .comment_base import CommentBase


class CommentCreate(CommentBase):
    post_id: int
    user_id: Optional[int] = None
