import pytest
from unittest.mock import MagicMock, patch
from app import models
from tests_mock_db.conftest import create_mock_user, create_mock_post

class TestPosts:
    """Test suite for post endpoints"""

    def test_create_post_unauthenticated(self, client):
        """Test creating a post without authentication fails"""
        payload = {"title": "Test Post", "content": "Test content"}
        response = client.post("/posts/", json=payload)
        assert response.status_code == 401

    def test_create_post_authenticated(self, client, mock_db):
        """Test creating a post when authenticated"""
        from app.main import app
        from app.utils.auth_helper import get_current_user
        
        mock_user = create_mock_user(user_id=1, email="user@test.com")
        
        def override_get_current_user():
            return mock_user
        
        app.dependency_overrides[get_current_user] = override_get_current_user
        
        try:
            with patch('app.routers.posts.models.Post') as MockPost:
                mock_post = create_mock_post(post_id=1, title="Test Post", content="Test content", owner_id=1)
                MockPost.return_value = mock_post
                
                response = client.post("/posts/", json={
                    "title": "Test Post",
                    "content": "Test content"
                })
                
                assert response.status_code == 201
                mock_db.add.assert_called_once()
                mock_db.commit.assert_called_once()
        finally:
            app.dependency_overrides.pop(get_current_user, None)
    
    def test_list_posts_empty(self, client, mock_db):
        """Test listing posts when database is empty"""
        mock_query = MagicMock()
        mock_query.all.return_value = []
        mock_db.query.return_value = mock_query
        
        response = client.get("/posts/")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_posts_with_data(self, client, mock_db):
        """Test listing posts when posts exist"""
        
        mock_posts = [
            create_mock_post(1, "Post 1", "Content 1", owner_id=1),
            create_mock_post(2, "Post 2", "Content 2", owner_id=1),
            create_mock_post(3, "Post 3", "Content 3", owner_id=2)
        ]
        
        mock_query = MagicMock()
        mock_query.all.return_value = mock_posts
        mock_db.query.return_value = mock_query
        
        response = client.get("/posts/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert all("id" in post for post in data)
        assert all("title" in post for post in data)

    def test_get_post_by_id_success(self, client, mock_db):
        """Test getting a specific post by ID"""
        
        mock_post = create_mock_post(1, "Test Post", "Test content", owner_id=1)
        
        mock_query = MagicMock()
        mock_query.get.return_value = mock_post
        mock_db.query.return_value = mock_query
        
        response = client.get("/posts/1")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Post"
        assert data["content"] == "Test content"

    def test_get_post_not_found(self, client, mock_db):
        """Test getting a post that doesn't exist"""
        
        mock_query = MagicMock()
        mock_query.get.return_value = None
        mock_db.query.return_value = mock_query
        
        response = client.get("/posts/99999")
        assert response.status_code == 404

    def test_update_post_unauthenticated(self, client):
        """Test updating a post without authentication fails"""
        response = client.put("/posts/1", json={
            "title": "Updated Title",
            "content": "Updated content"
        })
        assert response.status_code == 401

    def test_delete_post_unauthenticated(self, client):
        """Test deleting a post without authentication fails"""
        response = client.delete("/posts/1")
        assert response.status_code == 401

    def test_delete_post_as_owner(self, client, mock_db):
        """Test deleting a post as the owner"""
        from app.main import app
        from app.utils.auth_helper import get_current_user
        
        mock_user = create_mock_user(user_id=1)
        mock_post = create_mock_post(1, "Test Post", "Content", owner_id=1)
        
        mock_query = MagicMock()
        mock_query.get.return_value = mock_post
        mock_db.query.return_value = mock_query
        
        def override_get_current_user():
            return mock_user
        
        app.dependency_overrides[get_current_user] = override_get_current_user
        
        try:
            response = client.delete("/posts/1")
            
            assert response.status_code in [200, 204]
            mock_db.delete.assert_called_once_with(mock_post)
            mock_db.commit.assert_called_once()
        finally:
            app.dependency_overrides.pop(get_current_user, None)
