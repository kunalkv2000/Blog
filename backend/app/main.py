from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from .database import Base, engine
from . import models
from .routers import users, posts, comments, auth

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blog API Service")

origins = [
    os.getenv("FRONTEND_URL"),
    os.getenv("FRONTEND_IP_URL")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(auth.router)     
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)


@app.get("/")
def root():
    return {"message": "Blog API is running"}
