# app/utils/file_utils.py
import os
from typing import Optional
from fastapi import UploadFile, HTTPException
from app.config import settings
from app.utils.logger import logger

def validate_file_type(filename: str) -> bool:
    """
    Check if file type is allowed
    
    Args:
        filename: Name of the file
        
    Returns:
        True if allowed, False otherwise
    """
    ext = filename.split('.')[-1].lower()
    return ext in settings.allowed_file_types_list

def validate_file_size(file_size: int) -> bool:
    """
    Check if file size is within limits
    
    Args:
        file_size: Size of file in bytes
        
    Returns:
        True if within limits, False otherwise
    """
    return file_size <= settings.max_file_size_bytes

async def save_upload_file(upload_file: UploadFile) -> str:
    """
    Save uploaded file to disk
    
    Args:
        upload_file: FastAPI UploadFile object
        
    Returns:
        Path to saved file
        
    Raises:
        HTTPException: If file validation fails
    """
    # Validate file type
    if not validate_file_type(upload_file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {settings.ALLOWED_FILE_TYPES}"
        )
    
    # Read file content
    content = await upload_file.read()
    file_size = len(content)
    
    # Validate file size
    if not validate_file_size(file_size):
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE_MB}MB"
        )
    
    # Generate unique filename
    import uuid
    unique_filename = f"{uuid.uuid4()}_{upload_file.filename}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
    
    # Save file
    try:
        with open(file_path, "wb") as f:
            f.write(content)
        logger.info(f"File saved: {file_path}")
        return file_path
    except Exception as e:
        logger.error(f"Error saving file: {e}")
        raise HTTPException(status_code=500, detail="Error saving file")

def delete_file(file_path: str) -> None:
    """
    Delete file from disk
    
    Args:
        file_path: Path to file
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"File deleted: {file_path}")
    except Exception as e:
        logger.error(f"Error deleting file: {e}")