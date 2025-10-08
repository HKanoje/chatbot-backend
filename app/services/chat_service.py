# app/services/chat_service.py
from typing import Dict, Optional
from fastapi import UploadFile
from app.core.rag_engine import rag_engine
from app.utils.file_utils import save_upload_file
from app.utils.logger import logger

class ChatService:
    """Business logic for chat operations"""
    
    def __init__(self):
        """Initialize chat service"""
        self.rag_engine = rag_engine
    
    async def handle_chat_message(
        self,
        message: str,
        conversation_id: Optional[str] = None
    ) -> Dict:
        """
        Handle chat message and generate response
        
        Args:
            message: User's message
            conversation_id: Optional conversation ID
            
        Returns:
            Response dict
        """
        try:
            logger.info(f"Handling chat message: {message[:50]}...")
            
            # Use RAG engine to process query
            result = await self.rag_engine.query(
                user_query=message,
                conversation_id=conversation_id
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error in chat service: {e}")
            raise Exception(f"Failed to process message: {str(e)}")
    
    async def handle_file_upload(self, file: UploadFile) -> Dict:
        """
        Handle document upload and processing
        
        Args:
            file: Uploaded file
            
        Returns:
            Processing result dict
        """
        try:
            logger.info(f"Handling file upload: {file.filename}")
            
            # Save file
            file_path = await save_upload_file(file)
            
            # Process and store document
            result = await self.rag_engine.process_and_store_document(file_path)
            
            return result
            
        except Exception as e:
            logger.error(f"Error handling file upload: {e}")
            raise Exception(f"Failed to process file: {str(e)}")
    
    async def get_stats(self) -> Dict:
        """
        Get vector store statistics
        
        Returns:
            Statistics dict
        """
        try:
            return await self.rag_engine.get_collection_stats()
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {'error': str(e)}

# Create global instance
chat_service = ChatService()