 # app/services/file_service.py
from typing import List
from fastapi import UploadFile
from app.utils.file_utils import save_upload_file, validate_file_type
from app.utils.logger import logger

class FileService:
    """Service for file operations"""
    
    async def validate_and_save_file(self, file: UploadFile) -> str:
        """
        Validate and save uploaded file
        
        Args:
            file: Uploaded file
            
        Returns:
            Path to saved file
        """
        try:
            # Validate file type
            if not validate_file_type(file.filename):
                raise ValueError(f"Invalid file type: {file.filename}")
            
            # Save file
            file_path = await save_upload_file(file)
            logger.info(f"File saved: {file_path}")
            
            return file_path
            
        except Exception as e:
            logger.error(f"Error in file service: {e}")
            raise

# Create global instance
file_service = FileService()