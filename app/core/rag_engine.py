# app/core/rag_engine.py
from typing import List, Dict, Optional
from app.core.llm_client import gemini_client
from app.core.vector_store import vector_store
from app.core.document_processor import document_processor
from app.utils.logger import logger
from app.utils.file_utils import delete_file
import uuid

class RAGEngine:
    """Main RAG (Retrieval Augmented Generation) engine"""
    
    def __init__(self):
        """Initialize RAG engine"""
        self.llm_client = gemini_client
        self.vector_store = vector_store
        self.document_processor = document_processor
        logger.info("RAG Engine initialized")
    
    async def process_and_store_document(self, file_path: str) -> Dict:
        """
        Process document and store in vector database
        
        Args:
            file_path: Path to uploaded document
            
        Returns:
            Processing result dict
        """
        try:
            # Extract text chunks and metadata
            chunks, base_metadata = await self.document_processor.process_document(file_path)
            
            if not chunks:
                raise ValueError("No text chunks extracted from document")
            
            # Generate embeddings for each chunk
            logger.info(f"Generating embeddings for {len(chunks)} chunks")
            embeddings = []
            for chunk in chunks:
                embedding = await self.llm_client.generate_embeddings(chunk)
                embeddings.append(embedding)
            
            # Prepare metadata for each chunk
            metadata_list = []
            for i in range(len(chunks)):
                chunk_metadata = base_metadata.copy()
                chunk_metadata['chunk_index'] = i
                metadata_list.append(chunk_metadata)
            
            # Store in vector database
            doc_ids = await self.vector_store.add_documents(
                texts=chunks,
                embeddings=embeddings,
                metadata=metadata_list
            )
            
            # Clean up uploaded file
            delete_file(file_path)
            
            logger.info(f"Document processed successfully: {base_metadata['filename']}")
            
            return {
                'success': True,
                'message': 'Document processed and stored successfully',
                'document_ids': doc_ids,
                'filename': base_metadata['filename'],
                'chunks_count': len(chunks)
            }
            
        except Exception as e:
            logger.error(f"Error processing document: {e}")
            # Clean up file on error
            delete_file(file_path)
            raise
    
    async def query(
        self, 
        user_query: str, 
        conversation_id: Optional[str] = None,
        top_k: int = 5
    ) -> Dict:
        """
        Answer user query using RAG
        
        Args:
            user_query: User's question
            conversation_id: Optional conversation ID
            top_k: Number of relevant chunks to retrieve
            
        Returns:
            Response dict with answer and sources
        """
        try:
            # Generate conversation ID if not provided
            if not conversation_id:
                conversation_id = str(uuid.uuid4())
            
            logger.info(f"Processing query: {user_query[:50]}...")
            
            # Generate query embedding
            query_embedding = await self.llm_client.generate_query_embedding(user_query)
            
            # Search for relevant documents
            search_results = await self.vector_store.search(
                query_embedding=query_embedding,
                top_k=top_k
            )
            
            if not search_results:
                # No documents in database, respond without context
                response = await self.llm_client.generate_response(
                    f"Answer this question: {user_query}\n\n"
                    "Note: No reference documents are available."
                )
                return {
                    'response': response,
                    'conversation_id': conversation_id,
                    'sources': [],
                    'has_context': False
                }
            
            # Extract relevant context
            context_chunks = [result['text'] for result in search_results]
            sources = list(set([result['metadata'].get('filename', 'Unknown') 
                               for result in search_results]))
            
            # Generate response using RAG
            response = await self.llm_client.generate_rag_response(
                query=user_query,
                context=context_chunks
            )
            
            logger.info(f"Query answered successfully. Used {len(sources)} sources")
            
            return {
                'response': response,
                'conversation_id': conversation_id,
                'sources': sources,
                'has_context': True,
                'relevance_scores': [result['score'] for result in search_results]
            }
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            raise
    
    async def get_collection_stats(self) -> Dict:
        """
        Get statistics about the vector store
        
        Returns:
            Statistics dict
        """
        try:
            return self.vector_store.get_collection_info()
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {'error': str(e)}

# Create global instance
rag_engine = RAGEngine()