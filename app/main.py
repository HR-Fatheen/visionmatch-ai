from fastapi import FastAPI

from app.database import Base, engine
from app.models import (
    Image,
    ImageVector,
    MatchResult,
    Post,
    PostVector,
    Review,
)


app = FastAPI(
    title="AI Image Understanding & Content Matching Engine",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "name": "AI Image Understanding & Content Matching Engine",
        "status": "running",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}