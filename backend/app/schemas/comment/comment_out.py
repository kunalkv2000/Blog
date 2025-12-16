from typing import Optional
from pydantic import ConfigDict
from .comment import Comment


class CommentOut(Comment):
    author_name: Optional[str] = None
    author_avatar: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
