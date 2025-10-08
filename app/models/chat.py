# app/models/chat.py
from pydantic import BaseModel, Field
from typing import Optional, List

class ChatRequest(BaseModel):
    """Chat request model"""
    message: str = Field(..., min_length=1, max_length=5000, description="User message")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for context")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "What is the main topic of the uploaded document?",
                "conversation_id": "abc123"
            }
        }

class ChatResponse(BaseModel):
    """Chat response model"""
    response: str = Field(..., description="Bot response")
    conversation_id: str = Field(..., description="Conversation ID")
    sources: Optional[List[str]] = Field(default=[], description="Source documents used")
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "Based on the document, the main topic is...",
                "conversation_id": "abc123",
                "sources": ["document1.pdf", "document2.txt"]
            }
        }

class ErrorResponse(BaseModel):
    """Error response model"""
    detail: str = Field(..., description="Error message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "detail": "An error occurred while processing your request"
            }
        }