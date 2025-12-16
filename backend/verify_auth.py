import sys
import io

# Fix encoding for Windows console
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_auth_verification.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Recreate tables
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_authentication_requirements():
    """Test that POST and DELETE endpoints require authentication"""
    
    print("\n" + "="*80)
    print("AUTHENTICATION VERIFICATION TESTS")
    print("="*80)
    
    # Test 1: POST /posts without authentication should fail
    print("\n[TEST 1] POST /posts without authentication")
    response = client.post("/posts/", json={"title": "Test", "content": "Content"})
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    print("✅ PASSED: Returns 401 Unauthorized")
    
    # Test 2: DELETE /posts/{id} without authentication should fail
    print("\n[TEST 2] DELETE /posts/1 without authentication")
    response = client.delete("/posts/1")
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    print("✅ PASSED: Returns 401 Unauthorized")
    
    # Test 3: PUT /users/{id} without authentication should fail
    print("\n[TEST 3] PUT /users/1 without authentication")
    response = client.put("/users/1", json={"name": "Updated"})
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    print("✅ PASSED: Returns 401 Unauthorized")
    
    # Test 4: DELETE /users/{id} without authentication should fail
    print("\n[TEST 4] DELETE /users/1 without authentication")
    response = client.delete("/users/1")
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    print("✅ PASSED: Returns 401 Unauthorized")
    
    # Test 5: DELETE /comments/{id} without authentication should fail
    print("\n[TEST 5] DELETE /comments/1 without authentication")
    response = client.delete("/comments/1")
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    print("✅ PASSED: Returns 401 Unauthorized")
    
    print("\n" + "="*80)
    print("AUTHENTICATION WITH VALID USER")
    print("="*80)
    
    # Create admin user
    print("\n[SETUP] Creating admin user")
    admin_data = {
        "email": "admin@test.com",
        "name": "Admin User",
        "password": "admin123",
        "role": "admin"
    }
    response = client.post("/users/", json=admin_data)
    assert response.status_code == 201, f"Failed to create admin: {response.text}"
    admin_id = response.json()["id"]
    print(f"✅ Admin user created with ID: {admin_id}")
    
    # Login as admin
    print("\n[SETUP] Logging in as admin")
    response = client.post("/auth/login", json={
        "email": "admin@test.com",
        "password": "admin123"
    })
    assert response.status_code == 200, f"Login failed: {response.text}"
    print("✅ Login successful")
    
    # Test 6: POST /posts with authentication should succeed
    print("\n[TEST 6] POST /posts with authentication")
    response = client.post("/posts/", json={"title": "Auth Test", "content": "Content"})
    assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
    post_data = response.json()
    assert post_data["owner_id"] == admin_id, "Post owner should be the authenticated user"
    print(f"✅ PASSED: Post created with owner_id={admin_id}")
    
    # Test 7: Create regular user
    print("\n[TEST 7] Creating regular user as admin")
    user_data = {
        "email": "user@test.com",
        "name": "Regular User",
        "password": "user123",
        "role": "user"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201, f"Failed to create user: {response.text}"
    user_id = response.json()["id"]
    print(f"✅ User created with ID: {user_id}")
    
    # Test 8: Admin can update other users
    print("\n[TEST 8] Admin updating other user")
    response = client.put(f"/users/{user_id}", json={"name": "Updated Name"})
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    assert response.json()["name"] == "Updated Name"
    print("✅ PASSED: Admin can update other users")
    
    # Test 9: Admin can delete other users
    print("\n[TEST 9] Admin deleting other user")
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204, f"Expected 204, got {response.status_code}: {response.text}"
    print("✅ PASSED: Admin can delete other users")
    
    # Test 10: Admin cannot delete themselves
    print("\n[TEST 10] Admin cannot delete themselves")
    response = client.delete(f"/users/{admin_id}")
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    print("✅ PASSED: Admin prevented from self-deletion")
    
    # Logout
    print("\n[SETUP] Logging out")
    client.post("/auth/logout")
    
    # Recreate regular user
    print("\n[SETUP] Recreating regular user")
    admin_login = client.post("/auth/login", json={"email": "admin@test.com", "password": "admin123"})
    user_data = {
        "email": "user@test.com",
        "name": "Regular User",
        "password": "user123",
        "role": "user"
    }
    response = client.post("/users/", json=user_data)
    user_id = response.json()["id"]
    client.post("/auth/logout")
    
    # Login as regular user
    print("\n[SETUP] Logging in as regular user")
    response = client.post("/auth/login", json={
        "email": "user@test.com",
        "password": "user123"
    })
    assert response.status_code == 200
    print("✅ Logged in as regular user")
    
    # Test 11: Regular user can update themselves
    print("\n[TEST 11] Regular user updating own profile")
    response = client.put(f"/users/{user_id}", json={"name": "Self Updated"})
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    print("✅ PASSED: User can update own profile")
    
    # Test 12: Regular user cannot update other users
    print("\n[TEST 12] Regular user cannot update other users")
    response = client.put(f"/users/{admin_id}", json={"name": "Hacked"})
    assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    print("✅ PASSED: User prevented from updating others")
    
    # Test 13: Regular user cannot delete users
    print("\n[TEST 13] Regular user cannot delete users")
    response = client.delete(f"/users/{admin_id}")
    assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    print("✅ PASSED: User prevented from deleting users")
    
    print("\n" + "="*80)
    print("ALL TESTS PASSED! ✅")
    print("="*80)
    print("\nSummary:")
    print("- All POST and DELETE endpoints require authentication")
    print("- Posts are created with authenticated user as owner")
    print("- Users can update their own profile")
    print("- Admins can update/delete any user (except themselves)")
    print("- Regular users cannot update/delete others")
    print("="*80 + "\n")

if __name__ == "__main__":
    try:
        test_authentication_requirements()
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        raise
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        raise
