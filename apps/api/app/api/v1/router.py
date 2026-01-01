from fastapi import APIRouter

from app.api.v1.endpoints import health, search, tags, words

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"], prefix="/health")
api_router.include_router(words.router, tags=["words"], prefix="/words")
api_router.include_router(tags.router, tags=["tags"], prefix="/tags")
api_router.include_router(search.router, tags=["search"], prefix="/search")
