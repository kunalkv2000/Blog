```
blog-api-service/
│
├── backend/
│   ├── requirements.txt
│   ├── .env
│   ├── main.py
│   │
│   ├── database.py
│   ├── config.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── post.py
│   │   ├── comment.py
│   │   └── auth.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   ├── posts.py
│   │   ├── comments.py
│   │   └── auth.py
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_users.py
│   │   ├── test_posts.py
│   │   └── test_comments.py
│   │
│   ├── postman_collection/
│   │   └── blog_api.postman_collection.json
│   │
│   └── utils/
│       ├── hashing.py
│       └── auth_helper.py
│
└── frontend/
    ├── package.json
    ├── vite.config.js
    ├── index.html
    │
    └── src/
        ├── main.jsx
        └── App.jsx
```

# Installation

cd backend
pip install -r requirements.txt

# DB Setup

# On Windows PowerShell:

```
$env:DATABASE_URL="postgresql+psycopg2://postgres:password@localhost:5432/blog_db"
```

# Run the background

```
uvicorn app.main:app --reload
```

# Backend endpoints (summary):

Root

- GET / - API health check

Auth

-

Users

- POST /users/ – create user

- GET /users/ – list users

- GET /users/{id} – get single user

Posts (full CRUD)

- POST /posts/ – create post

- GET /posts/ – list posts

- GET /posts/{id} – get single post

- PUT /posts/{id} – update post

- DELETE /posts/{id} – delete post

Comments

- POST /comments/ – create comment

- GET /comments/post/{post_id} – list comments for a post

# Run Test

pytest

# Run Frontend

```
cd frontend
npm create vite@latest blog-frontend -- --template react
cd blog-frontend
npm install
```

---

# Run Frontend

npm run dev

{
"email": "admin@blog.com",
"name": "Admin",
"password": "admin123",
"role": "admin"
}
