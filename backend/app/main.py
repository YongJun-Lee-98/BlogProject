# app/main.py
from fastapi import FastAPI
from app.api import auth, post  # 📌 post 라우터 추가
from app.db.database import engine, Base

app = FastAPI()

# 라우터 등록
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(
    post.router, prefix="/posts", tags=["posts"]
)  # 📌 게시글 라우터 등록

# DB 테이블 생성
Base.metadata.create_all(bind=engine)
