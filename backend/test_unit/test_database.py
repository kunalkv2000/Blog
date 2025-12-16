import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

from app.database import Base
from app.models import User, Post, Comment

# Test database (SQLite file)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_database.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Password hashing
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Create test tables
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


@pytest.fixture(autouse=True)
def clear_tables():
    # Cleanup before each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_user_model_creation():
    """Test creating a User model directly via SQLAlchemy"""
    db = TestingSessionLocal()
    
    # Create user
    user = User(
        email="test@example.com",
        name="Test User",
        password_hash=pwd_context.hash("password123"),
        role="user"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Assertions
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.name == "Test User"
    assert user.role == "user"
    assert user.password_hash is not None
    assert user.created_at is not None
    
    db.close()


def test_user_unique_email_constraint():
    """Test that duplicate email addresses are not allowed"""
    db = TestingSessionLocal()
    
    # Create first user
    user1 = User(
        email="duplicate@example.com",
        name="User One",
        password_hash=pwd_context.hash("pass123"),
        role="user"
    )
    db.add(user1)
    db.commit()
    
    # Try to create second user with same email
    user2 = User(
        email="duplicate@example.com",
        name="User Two",
        password_hash=pwd_context.hash("pass456"),
        role="user"
    )
    db.add(user2)
    
    # Assertions - should raise IntegrityError
    with pytest.raises(IntegrityError):
        db.commit()
    
    db.close()


def test_post_model_creation():
    """Test creating a Post model"""
    db = TestingSessionLocal()
    
    # Create user first
    user = User(
        email="author@example.com",
        name="Author",
        password_hash=pwd_context.hash("pass123"),
        role="user"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create post
    post = Post(
        title="My First Post",
        content="This is the content of my post.",
        owner_id=user.id
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    
    # Assertions
    assert post.id is not None
    assert post.title == "My First Post"
    assert post.content == "This is the content of my post."
    assert post.owner_id == user.id
    assert post.created_at is not None
    
    db.close()


def test_comment_model_creation():
    """Test creating a Comment model"""
    db = TestingSessionLocal()
    
    # Create user and post
    user = User(
        email="commenter@example.com",
        name="Commenter",
        password_hash=pwd_context.hash("pass123"),
        role="user"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    post = Post(
        title="Post for Comments",
        content="Content here",
        owner_id=user.id
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    
    # Create comment
    comment = Comment(
        content="This is a great post!",
        post_id=post.id,
        user_id=user.id
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    
    # Assertions
    assert comment.id is not None
    assert comment.content == "This is a great post!"
    assert comment.post_id == post.id
    assert comment.user_id == user.id
    assert comment.created_at is not None
    
    db.close()


def test_user_posts_relationship():
    """Test User-Posts relationship (one-to-many)"""
    db = TestingSessionLocal()
    
    # Create user
    user = User(
        email="blogger@example.com",
        name="Blogger",
        password_hash=pwd_context.hash("pass123"),
        role="user"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create multiple posts
    post1 = Post(title="Post 1", content="Content 1", owner_id=user.id)
    post2 = Post(title="Post 2", content="Content 2", owner_id=user.id)
    post3 = Post(title="Post 3", content="Content 3", owner_id=user.id)
    db.add_all([post1, post2, post3])
    db.commit()
    
    # Refresh user to load relationship
    db.refresh(user)
    
    # Assertions
    assert len(user.posts) == 3
    post_titles = [p.title for p in user.posts]
    assert "Post 1" in post_titles
    assert "Post 2" in post_titles
    assert "Post 3" in post_titles
    
    db.close()


def test_user_comments_relationship():
    """Test User-Comments relationship (one-to-many)"""
    db = TestingSessionLocal()
    
    # Create user and a post
    user = User(
        email="commenter@example.com",
        name="Commenter",
        password_hash=pwd_context.hash("pass123"),
        role="user"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    post = Post(title="Post", content="Content", owner_id=user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    
    # Create multiple comments
    comment1 = Comment(content="Comment 1", post_id=post.id, user_id=user.id)
    comment2 = Comment(content="Comment 2", post_id=post.id, user_id=user.id)
    db.add_all([comment1, comment2])
    db.commit()
    
    # Refresh user to load relationship
    db.refresh(user)
    
    # Assertions
    assert len(user.comments) == 2
    comment_contents = [c.content for c in user.comments]
    assert "Comment 1" in comment_contents
    assert "Comment 2" in comment_contents
    
    db.close()


def test_post_owner_relationship():
    """Test Post-User relationship (many-to-one)"""
    db = TestingSessionLocal()
    
    # Create user
    user = User(
        email="owner@example.com",
        name="Post Owner",
        password_hash=pwd_context.hash("pass123"),
        role="user"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create post
    post = Post(title="My Post", content="Content", owner_id=user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    
    # Assertions - verify owner relationship
    assert post.owner is not None
    assert post.owner.id == user.id
    assert post.owner.name == "Post Owner"
    assert post.owner.email == "owner@example.com"
    
    db.close()


def test_comment_author_relationship():
    """Test Comment-User relationship (many-to-one)"""
    db = TestingSessionLocal()
    
    # Create user and post
    user = User(
        email="author@example.com",
        name="Comment Author",
        password_hash=pwd_context.hash("pass123"),
        role="user"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    post = Post(title="Post", content="Content", owner_id=user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    
    # Create comment
    comment = Comment(content="My comment", post_id=post.id, user_id=user.id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    
    # Assertions - verify author relationship
    assert comment.author is not None
    assert comment.author.id == user.id
    assert comment.author.name == "Comment Author"
    
    db.close()


def test_cascade_delete_user_posts():
    """Test that deleting a user cascades to delete their posts"""
    db = TestingSessionLocal()
    
    # Create user with posts
    user = User(
        email="cascade@example.com",
        name="Cascade User",
        password_hash=pwd_context.hash("pass123"),
        role="user"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    user_id = user.id
    
    # Create posts
    post1 = Post(title="Post 1", content="Content 1", owner_id=user.id)
    post2 = Post(title="Post 2", content="Content 2", owner_id=user.id)
    db.add_all([post1, post2])
    db.commit()
    
    # Verify posts exist
    posts_before = db.query(Post).filter(Post.owner_id == user_id).all()
    assert len(posts_before) == 2
    
    # Delete user
    db.delete(user)
    db.commit()
    
    # Assertions - posts should be deleted due to cascade
    posts_after = db.query(Post).filter(Post.owner_id == user_id).all()
    assert len(posts_after) == 0
    
    db.close()


def test_cascade_delete_user_comments():
    """Test that deleting a user cascades to delete their comments"""
    db = TestingSessionLocal()
    
    # Create user with comments
    user = User(
        email="cascade@example.com",
        name="Cascade User",
        password_hash=pwd_context.hash("pass123"),
        role="user"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    user_id = user.id
    
    # Create post
    post = Post(title="Post", content="Content", owner_id=user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    
    # Create comments
    comment1 = Comment(content="Comment 1", post_id=post.id, user_id=user.id)
    comment2 = Comment(content="Comment 2", post_id=post.id, user_id=user.id)
    db.add_all([comment1, comment2])
    db.commit()
    
    # Verify comments exist
    comments_before = db.query(Comment).filter(Comment.user_id == user_id).all()
    assert len(comments_before) == 2
    
    # Delete user
    db.delete(user)
    db.commit()
    
    # Assertions - comments should be deleted due to cascade
    comments_after = db.query(Comment).filter(Comment.user_id == user_id).all()
    assert len(comments_after) == 0
    
    db.close()


def test_user_query_operations():
    """Test basic CRUD operations on User model"""
    db = TestingSessionLocal()
    
    # CREATE
    user = User(
        email="crud@example.com",
        name="CRUD User",
        password_hash=pwd_context.hash("pass123"),
        role="user"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    user_id = user.id
    
    # READ
    fetched_user = db.query(User).filter(User.id == user_id).first()
    assert fetched_user is not None
    assert fetched_user.email == "crud@example.com"
    
    # UPDATE
    fetched_user.name = "Updated Name"
    db.commit()
    db.refresh(fetched_user)
    assert fetched_user.name == "Updated Name"
    
    # DELETE
    db.delete(fetched_user)
    db.commit()
    deleted_user = db.query(User).filter(User.id == user_id).first()
    assert deleted_user is None
    
    db.close()


def test_query_by_email():
    """Test querying users by email"""
    db = TestingSessionLocal()
    
    # Create users
    user1 = User(email="alice@test.com", name="Alice", password_hash=pwd_context.hash("pass"), role="user")
    user2 = User(email="bob@test.com", name="Bob", password_hash=pwd_context.hash("pass"), role="user")
    db.add_all([user1, user2])
    db.commit()
    
    # Query by email
    alice = db.query(User).filter(User.email == "alice@test.com").first()
    bob = db.query(User).filter(User.email == "bob@test.com").first()
    
    # Assertions
    assert alice is not None
    assert alice.name == "Alice"
    assert bob is not None
    assert bob.name == "Bob"
    
    db.close()


def test_query_by_role():
    """Test querying users by role"""
    db = TestingSessionLocal()
    
    # Create users with different roles
    admin1 = User(email="admin1@test.com", name="Admin 1", password_hash=pwd_context.hash("pass"), role="admin")
    admin2 = User(email="admin2@test.com", name="Admin 2", password_hash=pwd_context.hash("pass"), role="admin")
    user1 = User(email="user1@test.com", name="User 1", password_hash=pwd_context.hash("pass"), role="user")
    db.add_all([admin1, admin2, user1])
    db.commit()
    
    # Query admins
    admins = db.query(User).filter(User.role == "admin").all()
    
    # Assertions
    assert len(admins) == 2
    admin_names = [a.name for a in admins]
    assert "Admin 1" in admin_names
    assert "Admin 2" in admin_names
    
    db.close()
