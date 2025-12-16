import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, Mock, patch
from passlib.context import CryptContext
from app.main import app
from app.database import get_db
from app.models.user_model import User
from app.models.post_model import Post
from app.models.comment_model import Comment


# Password hashing context for tests
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


@pytest.fixture
def mock_db():
    """Create a mock database session"""
    db = MagicMock()
    return db


def create_mock_user(user_id=1, email="test@example.com", name="Test User", password="testpass", role="user"):
    """Helper function to create a mock user object"""
    from datetime import datetime
    mock_user = Mock(spec=User)
    mock_user.id = user_id
    mock_user.email = email
    mock_user.name = name
    mock_user.password_hash = pwd_context.hash(password)
    mock_user.role = role
    mock_user.created_at = datetime.now()
    return mock_user


def create_mock_post(post_id=1, title="Test Post", content="Test content", owner_id=1):
    """Helper function to create a mock post object"""
    from datetime import datetime
    mock_post = Mock(spec=Post)
    mock_post.id = post_id
    mock_post.title = title
    mock_post.content = content
    mock_post.owner_id = owner_id
    mock_post.created_at = datetime.now()
    return mock_post


def create_mock_comment(comment_id=1, content="Test comment", post_id=1, user_id=1):
    """Helper function to create a mock comment object"""
    from datetime import datetime
    mock_comment = Mock(spec=Comment)
    mock_comment.id = comment_id
    mock_comment.content = content
    mock_comment.post_id = post_id
    mock_comment.user_id = user_id
    mock_comment.created_at = datetime.now()
    return mock_comment


@pytest.fixture
def client(mock_db):
    """Create a test client with mocked database"""
    def override_get_db():
        try:
            yield mock_db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up
    app.dependency_overrides.clear()


@pytest.fixture
def mock_pwd_context():
    """Mock password context for testing"""
    return pwd_context
