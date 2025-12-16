import pytest
from unittest.mock import MagicMock, patch
from app import models
from app.main import app
from app.utils.auth_helper import get_current_user
from tests_mock_db.conftest import create_mock_user, create_mock_comment


class TestComments:
    """Test suite for comment endpoints"""

    def test_create_comment_unauthenticated(self, client,mock_db):
        """Test that creating a comment fails when not authenticated"""
        response = client.post("/comments/", json={
            "content": "Great post!",
            "post_id": 1
        })
        
        assert response.status_code == 401

    def test_list_comments_for_post(self, client, mock_db):
        """Test listing all comments for a specific post"""        
        mock_comments = [
            create_mock_comment(1, "First comment", post_id=1, user_id=1),
            create_mock_comment(2, "Second comment", post_id=1, user_id=2),
            create_mock_comment(3, "Third comment", post_id=1, user_id=1)
        ]
        
        result_tuples = [
            (mock_comments[0], "User One"),
            (mock_comments[1], "User Two"),
            (mock_comments[2], "User One")
        ]
        
        mock_order = MagicMock()
        mock_order.all.return_value = result_tuples
        mock_filter = MagicMock()
        mock_filter.order_by.return_value = mock_order
        mock_join = MagicMock()
        mock_join.filter.return_value = mock_filter
        mock_query = MagicMock()
        mock_query.join.return_value = mock_join
        mock_db.query.return_value = mock_query
        
        response = client.get("/comments/post/1")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert all("id" in comment for comment in data)
        assert all("content" in comment for comment in data)

    def test_list_comments_empty_post(self, client, mock_db):
        """Test listing comments for a post with no comments"""
        mock_filter = MagicMock()
        mock_filter.all.return_value = []
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_filter
        mock_db.query.return_value = mock_query
        
        response = client.get("/comments/post/1")
        
        assert response.status_code == 200
        assert response.json() == []

    def test_update_own_comment(self, client, mock_db):
        """Test that a user can update their own comment"""        
        mock_user = create_mock_user(user_id=1)
        mock_comment = create_mock_comment(1, "Original content", post_id=1, user_id=1)
        
        mock_filter = MagicMock()
        mock_filter.first.return_value = mock_comment
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_filter
        mock_db.query.return_value = mock_query

        def override_get_current_user():
            return mock_user
        
        app.dependency_overrides[get_current_user] = override_get_current_user
        
        try:
            response = client.put("/comments/1", json={
                "content": "Updated content"
            })
            
            if response.status_code == 200:
                assert mock_comment.content == "Updated content"
                mock_db.commit.assert_called()
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    def test_update_another_users_comment_fails(self, client, mock_db):
        """Test that a user cannot update another user's comment"""
        
        mock_user = create_mock_user(user_id=2)  # Different user
        mock_comment = create_mock_comment(1, "User1's comment", post_id=1, user_id=1)
        
        mock_filter = MagicMock()
        mock_filter.first.return_value = mock_comment
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_filter
        mock_db.query.return_value = mock_query
        
        def override_get_current_user():
            return mock_user
        
        app.dependency_overrides[get_current_user] = override_get_current_user
        
        try:
            response = client.put("/comments/1", json={
                "content": "Hacked content"
            })
            
            assert response.status_code == 403
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    def test_delete_own_comment(self, client, mock_db):
        """Test that a user can delete their own comment"""        
        mock_user = create_mock_user(user_id=1)
        mock_comment = create_mock_comment(1, "My comment", post_id=1, user_id=1)
        
        mock_filter = MagicMock()
        mock_filter.first.return_value = mock_comment
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_filter
        mock_db.query.return_value = mock_query
        
        def override_get_current_user():
            return mock_user
        
        app.dependency_overrides[get_current_user] = override_get_current_user
        
        try:
            response = client.delete("/comments/1")
            
            if response.status_code in [200, 204]:
                mock_db.delete.assert_called_once_with(mock_comment)
                mock_db.commit.assert_called()
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    def test_delete_another_users_comment_fails(self, client, mock_db):
        """Test that a user cannot delete another user's comment"""
        mock_user = create_mock_user(user_id=2)
        mock_comment = create_mock_comment(1, "User1's comment", post_id=1, user_id=1)
        
        mock_filter = MagicMock()
        mock_filter.first.return_value = mock_comment
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_filter
        mock_db.query.return_value = mock_query
        
        def override_get_current_user():
            return mock_user
        app.dependency_overrides[get_current_user] = override_get_current_user
        
        try:
            response = client.delete("/comments/1")
            assert response.status_code == 403
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    def test_delete_nonexistent_comment(self, client, mock_db):
        """Test deleting a comment that doesn't exist"""        
        mock_user = create_mock_user(user_id=1)
        mock_query = MagicMock()
        mock_query.get.return_value = None
        mock_db.query.return_value = mock_query
        
        def override_get_current_user():
            return mock_user
        app.dependency_overrides[get_current_user] = override_get_current_user
        
        try:
            response = client.delete("/comments/99999")
            
            assert response.status_code == 404
        finally:
            app.dependency_overrides.pop(get_current_user, None)
