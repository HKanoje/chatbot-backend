# app/models/document.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DocumentUploadResponse(BaseModel):
    """Response after document upload"""
    success: bool = Field(..., description="Upload success status")
    message: str = Field(..., description="Status message")
    document_id: Optional[str] = Field(None, description="Document ID in vector store")
    filename: str = Field(..., description="Original filename")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Document processed successfully",
                "document_id": "doc_123456",
                "filename": "example.pdf"
            }
        }

class DocumentMetadata(BaseModel):
    """Document metadata stored with vectors"""
    filename: str
    file_type: str
    upload_date: str
    chunk_index: int
    total_chunks: int