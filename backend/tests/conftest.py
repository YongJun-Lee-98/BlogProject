# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.db.database import Base, get_db
from app.db import models
from uuid import uuid4
from jose import jwt
from datetime import timedelta, datetime


# 테스트 전용 DB URL (SQLite 메모리 or 별도 파일 사용 가능)
TEST_DATABASE_URL = "sqlite:///./test.db"  # memory로 하려면 "sqlite://"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 테스트용 DB 연결로 오버라이드
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# app에 의존성 주입 오버라이드
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def create_test_user(db):
    user = models.User(
        id=uuid4(),
        username="testuser",
        email="test@example.com",
        hashed_password="$2b$12$8X5u/NL3f7XbK9zPH4IdGuuhmXZVToIq8jboOq8gQp4koC2cqdrba",  # bcrypt("1234")
    )
    db.add(user)
    db.commit()
    return user


@pytest.fixture
def access_token(create_test_user):
    payload = {
        "sub": str(create_test_user.id),
        "exp": datetime.utcnow() + timedelta(minutes=30),
    }
    return jwt.encode(payload, "your-secret-key", algorithm="HS256")
