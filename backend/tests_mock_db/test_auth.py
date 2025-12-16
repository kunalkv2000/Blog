import pytest
from app.main import app
from app.utils.auth_helper import get_current_user
from unittest.mock import MagicMock, patch
from app import models
from tests_mock_db.conftest import create_mock_user


class TestAuth:
    """Test suite for authentication endpoints"""

    def test_login_with_nonexistent_email(self, client, mock_db):
        """Test login fails with email that doesn't exist"""
        mock_filter = MagicMock()
        mock_filter.first.return_value = None
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_filter
        mock_db.query.return_value = mock_query
        
        response = client.post("/auth/login", json={
            "email": "nonexistent@test.com",
            "password": "anypassword"
        })
        
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"

    def test_login_with_wrong_password(self, client, mock_db):
        """Test login fails with wrong password"""

        mock_user = create_mock_user(
            user_id=1,
            email="test@example.com",
            password="correctpass"
        )
        
        mock_filter = MagicMock()
        mock_filter.first.return_value = mock_user
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_filter
        mock_db.query.return_value = mock_query
        
        response = client.post("/auth/login", json={
            "email": "test@example.com",
            "password": "wrongpass"
        })
        
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"

    def test_login_success(self, client, mock_db):
        """Test successful login with correct credentials"""
        
        mock_user = create_mock_user(
            user_id=1,
            email="test@example.com",
            name="Test User",
            password="testpass123",
            role="user"
        )
        
        mock_filter = MagicMock()
        mock_filter.first.return_value = mock_user
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_filter
        mock_db.query.return_value = mock_query
        
        response = client.post("/auth/login", json={
            "email": "test@example.com",
            "password": "testpass123"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["name"] == "Test User"
        assert data["role"] == "user"
        assert "id" in data
        assert "session" in response.cookies

    def test_logout(self, client):
        """Test logout clears the session cookie"""
        response = client.post("/auth/logout")
        
        assert response.status_code == 200
        assert response.json()["detail"] == "Logged out"

    def test_me_endpoint_unauthenticated(self, client):
        """Test /me endpoint fails when not authenticated"""
        response = client.get("/auth/me")
        assert response.status_code == 401
        
    def test_me_endpoint_authenticated(self, client, mock_db):
        """Test /me endpoint returns current user data when authenticated"""
        mock_user = create_mock_user(
            user_id=1,
            email="test@example.com",
            name="Test User",
            role="admin"
        )
        
        def override_get_current_user():
            return mock_user
        
        app.dependency_overrides[get_current_user] = override_get_current_user
        
        try:
            response = client.get("/auth/me")
            
            assert response.status_code == 200
            data = response.json()
            assert data["email"] == "test@example.com"
            assert data["name"] == "Test User"
            assert data["role"] == "admin"
            assert "id" in data
        finally:
            app.dependency_overrides.pop(get_current_user, None)
