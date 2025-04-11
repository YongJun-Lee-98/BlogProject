# app/api/post.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
import markdown2

from app.db import models
from app.db.database import get_db
from app.schemas import post as schemas
from app.core.security import get_current_user
from typing import List


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", response_model=schemas.PostResponse)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    html = markdown2.markdown(post.content_md)
    db_post = models.Post(
        title=post.title,
        slug=post.slug,
        content_md=post.content_md,
        content_html=html,
        author_id=current_user.id,
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.get("/{slug}", response_model=schemas.PostResponse)
def get_post_by_slug(slug: str, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.slug == slug).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.put("/{slug}", response_model=schemas.PostResponse)
def update_post(
    slug: str,
    update: schemas.PostUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    post = db.query(models.Post).filter(models.Post.slug == slug).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="권한이 없습니다")

    post.title = update.title
    post.slug = update.slug
    post.content_md = update.content_md
    post.content_html = markdown2.markdown(update.content_md)
    db.commit()
    db.refresh(post)
    return post


@router.delete("/{slug}")
def delete_post(
    slug: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    post = db.query(models.Post).filter(models.Post.slug == slug).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="권한이 없습니다")
    db.delete(post)
    db.commit()
    return {"message": "삭제 완료"}


@router.get("/", response_model=List[schemas.PostResponse])
def list_posts(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    posts = (
        db.query(models.Post)
        .order_by(models.Post.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return posts
