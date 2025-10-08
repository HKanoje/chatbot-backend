# app/api/dependencies.py
from fastapi import HTTPException, status
from app.utils.logger import logger

async def verify_api_health():
    """
    Dependency to verify API is healthy
    Can be extended to check database connections, etc.
    """
    try:
        # Add health checks here if needed
        return True
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service temporarily unavailable"
        )