# app/api/routes/chat.py
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, status
from typing import Optional
from app.models.chat import ChatRequest, ChatResponse, ErrorResponse
from app.models.document import DocumentUploadResponse
from app.services.chat_service import chat_service
from app.utils.logger import logger

router = APIRouter()

@router.post(
    "/chat",
    response_model=ChatResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Send chat message",
    description="Send a message and get AI response using RAG"
)
async def chat(request: ChatRequest):
    """
    Chat endpoint - send message and get response
    
    Args:
        request: Chat request with message and optional conversation_id
        
    Returns:
        AI response with sources
    """
    try:
        result = await chat_service.handle_chat_message(
            message=request.message,
            conversation_id=request.conversation_id
        )
        
        return ChatResponse(
            response=result['response'],
            conversation_id=result['conversation_id'],
            sources=result.get('sources', [])
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post(
    "/upload",
    response_model=DocumentUploadResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Upload document",
    description="Upload and process a document (PDF, Excel, Image, Text)"
)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload document endpoint
    
    Args:
        file: Document file to upload
        
    Returns:
        Upload status and document info
    """
    try:
        result = await chat_service.handle_file_upload(file)
        
        return DocumentUploadResponse(
            success=result['success'],
            message=result['message'],
            document_id=result['document_ids'][0] if result['document_ids'] else None,
            filename=result['filename']
        )
        
    except ValueError as e:
        # Client error (invalid file, etc.)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error in upload endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process document: {str(e)}"
        )

@router.post(
    "/chat-with-file",
    response_model=ChatResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Chat with file upload",
    description="Upload a file and ask a question about it in one request"
)
async def chat_with_file(
    message: str = Form(...),
    file: Optional[UploadFile] = File(None),
    conversation_id: Optional[str] = Form(None)
):
    """
    Combined endpoint - upload file and chat in one request
    
    Args:
        message: User's message
        file: Optional file to upload
        conversation_id: Optional conversation ID
        
    Returns:
        AI response
    """
    try:
        # Upload file if provided
        if file:
            logger.info(f"Processing file: {file.filename}")
            await chat_service.handle_file_upload(file)
        
        # Process chat message
        result = await chat_service.handle_chat_message(
            message=message,
            conversation_id=conversation_id
        )
        
        return ChatResponse(
            response=result['response'],
            conversation_id=result['conversation_id'],
            sources=result.get('sources', [])
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error in chat-with-file endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get(
    "/stats",
    summary="Get statistics",
    description="Get vector store statistics"
)
async def get_stats():
    """
    Get vector store statistics
    
    Returns:
        Statistics about stored documents
    """
    try:
        stats = await chat_service.get_stats()
        return stats
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )