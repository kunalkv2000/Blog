from datetime import datetime
from typing import Optional
from pydantic import ConfigDict
from .post_base import PostBase


class Post(PostBase):
    id: int
    owner_id: Optional[int]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
