from datetime import datetime
from typing import Optional
from pydantic import ConfigDict
from .comment_base import CommentBase


class Comment(CommentBase):
    id: int
    post_id: int
    user_id: Optional[int]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
