# app/api/routes/__init__.py
from fastapi import APIRouter
from app.api.routes import health, chat

# Create main API router
api_router = APIRouter()

# Include health routes (no prefix)
api_router.include_router(
    health.router,
    tags=["Health"]
)

# Include chat routes with prefix
api_router.include_router(
    chat.router,
    prefix="/api/v1",
    tags=["Chat"]
)