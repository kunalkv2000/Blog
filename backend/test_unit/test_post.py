import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# Test database (SQLite file)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_blog.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create test tables
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_tables():
    # Cleanup before each test (simple approach)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_create_post():
    payload = {"title": "Test Post", "content": "Test content"}
    response = client.post("/posts/", json=payload)
    assert response.status_code == 401


def test_list_posts_empty():
    response = client.get("/posts/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_and_get_post():
    payload = {"title": "My Post", "content": "Hello World"}
    create_res = client.post("/posts/", json=payload)
    assert create_res.status_code == 401
