# app/schemas/post.py
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class PostBase(BaseModel):
    title: str
    slug: str
    content_md: str


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class PostResponse(PostBase):
    id: UUID
    content_html: str
    author_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
