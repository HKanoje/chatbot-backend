# app/core/llm_client.py
import google.generativeai as genai
from typing import List, Dict
from app.config import settings
from app.utils.logger import logger

class GeminiClient:
    """Google Gemini LLM client"""
    
    def __init__(self):
        """Initialize Gemini client"""
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
            self.embedding_model = settings.GEMINI_EMBEDDING_MODEL
            logger.info("Gemini client initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Gemini client: {e}")
            raise
    
    async def generate_response(self, prompt: str) -> str:
        """
        Generate response from Gemini
        
        Args:
            prompt: Input prompt
            
        Returns:
            Generated response text
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise Exception(f"Failed to generate response: {str(e)}")
    
    async def generate_embeddings(self, text: str) -> List[float]:
        """
        Generate embeddings for text
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector
        """
        try:
            result = genai.embed_content(
                model=self.embedding_model,
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise Exception(f"Failed to generate embeddings: {str(e)}")
    
    async def generate_query_embedding(self, query: str) -> List[float]:
        """
        Generate embeddings for search query
        
        Args:
            query: Search query
            
        Returns:
            Embedding vector
        """
        try:
            result = genai.embed_content(
                model=self.embedding_model,
                content=query,
                task_type="retrieval_query"
            )
            return result['embedding']
        except Exception as e:
            logger.error(f"Error generating query embeddings: {e}")
            raise Exception(f"Failed to generate query embeddings: {str(e)}")
    
    async def generate_rag_response(
        self, 
        query: str, 
        context: List[str]
    ) -> str:
        """
        Generate response using RAG (Retrieval Augmented Generation)
        
        Args:
            query: User query
            context: List of relevant document chunks
            
        Returns:
            Generated response
        """
        # Build prompt with context
        context_text = "\n\n".join([f"Document {i+1}:\n{doc}" for i, doc in enumerate(context)])
        
        prompt = f"""You are a helpful AI assistant. Answer the user's question based on the provided context documents.

Context Documents:
{context_text}

User Question: {query}

Instructions:
- Answer based primarily on the context provided
- If the context doesn't contain enough information, say so
- Be concise and accurate
- Cite which document number you're referencing when relevant

Answer:"""
        
        try:
            response = await self.generate_response(prompt)
            return response
        except Exception as e:
            logger.error(f"Error generating RAG response: {e}")
            raise

# Create global instance
gemini_client = GeminiClient()