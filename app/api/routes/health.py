# app/api/routes/health.py
from fastapi import APIRouter
from datetime import datetime
from app.config import settings

router = APIRouter()

@router.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "status": "online"
    }

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION
    }

@router.get("/info")
async def info():
    """API information endpoint"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "RAG-based chatbot API using Google Gemini and Qdrant",
        "endpoints": {
            "chat": "/api/v1/chat",
            "upload": "/api/v1/upload",
            "stats": "/api/v1/stats"
        }
    }