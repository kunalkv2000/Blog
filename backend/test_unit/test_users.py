import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

from app.main import app
from app.database import Base, get_db
from app import models

# Test database (SQLite file)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_users.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Password hashing
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

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
    """Clear database before each test and reset app state"""
    # Setup: clear tables before test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # Reset dependency overrides to ensure clean state
    app.dependency_overrides[get_db] = override_get_db
    
    yield
    
    # Teardown: clear any remaining state
    app.dependency_overrides.clear()
    app.dependency_overrides[get_db] = override_get_db


def create_test_user(db, email="test@example.com", password="testpass123", role="user", name="Test User"):
    """Helper function to create a test user directly in the database"""
    hashed_password = pwd_context.hash(password)
    user = models.User(
        email=email,
        name=name,
        password_hash=hashed_password,
        role=role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(email, password):
    """Helper function to login and return the response with session cookie"""
    return client.post("/auth/login", json={
        "email": email,
        "password": password
    })


def test_create_first_user_no_auth_required():
    """Test that the first user can be created without authentication"""
    response = client.post("/users/", json={
        "email": "first@example.com",
        "name": "First User",
        "password": "password123",
        "role": "admin"
    })
    
    # Assertions
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "first@example.com"
    assert data["name"] == "First User"
    assert data["role"] == "admin"
    assert "id" in data
    assert "password_hash" not in data  # Should not expose password


def test_create_additional_user_requires_admin():
    """Test that creating a second user requires admin authentication"""
    # Create first user (admin)
    db = TestingSessionLocal()
    create_test_user(db, email="admin@test.com", password="admin123", role="admin")
    db.close()
    
    # Try to create another user without being logged in
    response = client.post("/users/", json={
        "email": "second@example.com",
        "name": "Second User",
        "password": "password123",
        "role": "user"
    })
    
    # Should fail with 401
    assert response.status_code == 401


def test_create_user_as_admin():
    """Test that admin can create additional users"""
    # Create first user (admin)
    db = TestingSessionLocal()
    create_test_user(db, email="admin@test.com", password="admin123", role="admin")
    db.close()
    
    # Login as admin
    login_response = login_user("admin@test.com", "admin123")
    assert login_response.status_code == 200
    
    # Create another user
    response = client.post("/users/", json={
        "email": "newuser@example.com",
        "name": "New User",
        "password": "password123",
        "role": "user"
    })
    
    # Assertions
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["name"] == "New User"
    assert data["role"] == "user"


def test_create_user_non_admin_fails():
    """Test that non-admin users cannot create new users"""
    # Create first admin user
    db = TestingSessionLocal()
    create_test_user(db, email="admin@test.com", password="admin123", role="admin")
    # Create a regular user
    create_test_user(db, email="user@test.com", password="user123", role="user")
    db.close()
    
    # Login as regular user
    login_response = login_user("user@test.com", "user123")
    assert login_response.status_code == 200
    
    # Try to create another user
    response = client.post("/users/", json={
        "email": "newuser@example.com",
        "name": "New User",
        "password": "password123",
        "role": "user"
    })
    
    # Should fail with 403
    assert response.status_code == 403


def test_create_duplicate_email():
    """Test that creating a user with duplicate email fails"""
    # Create first user
    client.post("/users/", json={
        "email": "user@test.com",
        "name": "User One",
        "password": "password123",
        "role": "admin"
    })
    
    # Try to create another user with same email
    response = client.post("/users/", json={
        "email": "user@test.com",
        "name": "User Two",
        "password": "password456",
        "role": "user"
    })
    
    # Assertions
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


def test_list_users():
    """Test listing all users"""
    # Create multiple users directly in DB
    db = TestingSessionLocal()
    create_test_user(db, email="user1@test.com", name="User One")
    create_test_user(db, email="user2@test.com", name="User Two")
    create_test_user(db, email="user3@test.com", name="User Three")
    db.close()
    
    # Get all users
    response = client.get("/users/")
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert all("email" in user for user in data)
    assert all("name" in user for user in data)
    
    emails = [user["email"] for user in data]
    assert "user1@test.com" in emails
    assert "user2@test.com" in emails
    assert "user3@test.com" in emails


def test_get_specific_user():
    """Test getting a specific user by ID"""
    # Create a user
    db = TestingSessionLocal()
    user = create_test_user(db, email="user@test.com", name="Specific User")
    user_id = user.id
    db.close()
    
    # Get the user
    response = client.get(f"/users/{user_id}")
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["email"] == "user@test.com"
    assert data["name"] == "Specific User"


def test_get_nonexistent_user():
    """Test getting a user that doesn't exist"""
    response = client.get("/users/99999")
    
    # Assertions
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]


def test_update_own_account():
    """Test that a user can update their own account"""
    # Create a user
    db = TestingSessionLocal()
    user = create_test_user(db, email="user@test.com", password="password123", name="Original Name")
    user_id = user.id
    db.close()
    
    # Login
    login_response = login_user("user@test.com", "password123")
    assert login_response.status_code == 200
    
    # Update own name
    response = client.put(f"/users/{user_id}", json={
        "name": "Updated Name"
    })
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["email"] == "user@test.com"


def test_update_another_user_as_admin():
    """Test that admin can update another user's information"""
    # Create admin and regular user
    db = TestingSessionLocal()
    admin = create_test_user(db, email="admin@test.com", password="admin123", role="admin")
    user = create_test_user(db, email="user@test.com", password="user123", role="user", name="Regular User")
    user_id = user.id
    db.close()
    
    # Login as admin
    login_response = login_user("admin@test.com", "admin123")
    assert login_response.status_code == 200
    
    # Update the regular user's role
    response = client.put(f"/users/{user_id}", json={
        "role": "admin",
        "name": "Promoted User"
    })
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "admin"
    assert data["name"] == "Promoted User"


def test_update_another_user_as_non_admin_fails():
    """Test that non-admin cannot update another user's information"""
    # Create two regular users
    db = TestingSessionLocal()
    user1 = create_test_user(db, email="user1@test.com", password="pass123", role="user")
    user2 = create_test_user(db, email="user2@test.com", password="pass123", role="user")
    user2_id = user2.id
    db.close()
    
    # Login as user1
    login_response = login_user("user1@test.com", "pass123")
    assert login_response.status_code == 200
    
    # Try to update user2
    response = client.put(f"/users/{user2_id}", json={
        "name": "Hacked Name"
    })
    
    # Assertions
    assert response.status_code == 403


def test_delete_user_as_admin():
    """Test that admin can delete other users"""
    # Create admin and regular user
    db = TestingSessionLocal()
    admin = create_test_user(db, email="admin@test.com", password="admin123", role="admin")
    user = create_test_user(db, email="user@test.com", password="user123", role="user")
    user_id = user.id
    db.close()
    
    # Login as admin
    login_response = login_user("admin@test.com", "admin123")
    assert login_response.status_code == 200
    
    # Delete the user
    response = client.delete(f"/users/{user_id}")
    
    # Assertions
    assert response.status_code == 204
    
    # Verify user is deleted
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404


def test_delete_user_as_non_admin_fails():
    """Test that non-admin cannot delete users"""
    # Create admin and regular user
    db = TestingSessionLocal()
    admin = create_test_user(db, email="admin@test.com", password="admin123", role="admin")
    user = create_test_user(db, email="user@test.com", password="user123", role="user")
    admin_id = admin.id
    db.close()
    
    # Login as regular user
    login_response = login_user("user@test.com", "user123")
    assert login_response.status_code == 200
    
    # Try to delete admin
    response = client.delete(f"/users/{admin_id}")
    
    # Assertions
    assert response.status_code == 403


def test_admin_cannot_delete_self():
    """Test that admin cannot delete their own account"""
    # Create admin
    db = TestingSessionLocal()
    admin = create_test_user(db, email="admin@test.com", password="admin123", role="admin")
    admin_id = admin.id
    db.close()
    
    # Login as admin
    login_response = login_user("admin@test.com", "admin123")
    assert login_response.status_code == 200
    
    # Try to delete self
    response = client.delete(f"/users/{admin_id}")
    
    # Assertions
    assert response.status_code == 400
    assert "Cannot delete your own account" in response.json()["detail"]
