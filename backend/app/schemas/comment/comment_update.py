from typing import Optional
from pydantic import BaseModel


class CommentUpdate(BaseModel):
    content: Optional[str] = None
