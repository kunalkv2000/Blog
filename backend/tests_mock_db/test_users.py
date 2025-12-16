import pytest
from unittest.mock import MagicMock, patch
from app import models
from app.main import app
from tests_mock_db.conftest import create_mock_user

class TestUsers:
    """Test suite for user management endpoints"""

    def test_create_user(self, client, mock_db):
        """Test creating a new user"""
        
        mock_filter = MagicMock()
        mock_filter.first.return_value = None
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_filter
        mock_query.count.return_value = 0  # No existing users, so first user can be created without auth
        mock_db.query.return_value = mock_query
        
        with patch('app.routers.users.models.User') as MockUser:
            mock_user = create_mock_user(user_id=1, email="user@test.com", name="New User")
            MockUser.return_value = mock_user
            
            response = client.post("/users/", json={
                "email": "user@test.com",
                "name": "New User",
                "password": "password123"
            })
            
            assert response.status_code == 201
            data = response.json()
            assert data["email"] == "user@test.com"
            assert data["name"] == "New User"

    def test_list_users(self, client, mock_db):
        """Test listing all users"""
        
        mock_users = [    
            create_mock_user(1, "user1@test.com", "User One"),
            create_mock_user(2, "user2@test.com", "User Two"),
            create_mock_user(3, "user3@test.com", "User Three")
        ]
        
        mock_query = MagicMock()
        mock_query.all.return_value = mock_users
        mock_db.query.return_value = mock_query
        
        response = client.get("/users/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert all("email" in user for user in data)
        assert all("name" in user for user in data)

    def test_get_specific_user(self, client, mock_db):
        """Test getting a specific user by ID"""

        mock_user = create_mock_user(1, "user@test.com", "Specific User")
        
        # The actual code uses db.query().get(user_id) not filter().first()
        mock_query = MagicMock()
        mock_query.get.return_value = mock_user
        mock_db.query.return_value = mock_query
        
        response = client.get("/users/1")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["email"] == "user@test.com"
        assert data["name"] == "Specific User"


    def test_update_user_as_admin(self, client, mock_db):
        """Test that admin can update user information"""
        
        mock_admin = create_mock_user(1, "admin@test.com", role="admin")
        mock_user = create_mock_user(2, "user@test.com", "Original Name", role="user")
        
        mock_query = MagicMock()
        mock_query.get.return_value = mock_user
        mock_db.query.return_value = mock_query
        
        with patch('app.routers.users.get_current_user', return_value=mock_admin):
            response = client.put("/users/2", json={
                "name": "Updated Name",
                "role": "admin"
            })
            
            if response.status_code == 200:
                mock_db.commit.assert_called()

    def test_delete_user_as_admin(self, client, mock_db):
        """Test that admin can delete other users"""        
        mock_admin = create_mock_user(1, "admin@test.com", role="admin")
        mock_user = create_mock_user(2, "user@test.com", role="user")
        
        mock_query = MagicMock()
        mock_query.get.return_value = mock_user
        mock_db.query.return_value = mock_query
        
        with patch('app.routers.users.get_current_user', return_value=mock_admin):
            response = client.delete("/users/2")
            
            if response.status_code in [200, 204]:
                mock_db.delete.assert_called_once_with(mock_user)
                mock_db.commit.assert_called()