# app/core/vector_store.py
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from typing import List, Dict, Optional
import uuid
from datetime import datetime
from app.config import settings
from app.utils.logger import logger

class VectorStore:
    """Qdrant vector database client"""
    
    def __init__(self):
        """Initialize Qdrant client"""
        try:
            self.client = QdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY,
            )
            self.collection_name = settings.QDRANT_COLLECTION_NAME
            self._ensure_collection_exists()
            logger.info("Qdrant client initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Qdrant client: {e}")
            raise
    
    def _ensure_collection_exists(self):
        """Create collection if it doesn't exist"""
        try:
            collections = self.client.get_collections().collections
            collection_names = [col.name for col in collections]
            
            if self.collection_name not in collection_names:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=settings.EMBEDDING_DIMENSION,
                        distance=Distance.COSINE
                    )
                )
                logger.info(f"Created collection: {self.collection_name}")
            else:
                logger.info(f"Collection already exists: {self.collection_name}")
        except Exception as e:
            logger.error(f"Error ensuring collection exists: {e}")
            raise
    
    async def add_documents(
        self,
        texts: List[str],
        embeddings: List[List[float]],
        metadata: List[Dict]
    ) -> List[str]:
        """
        Add documents to vector store
        
        Args:
            texts: List of text chunks
            embeddings: List of embedding vectors
            metadata: List of metadata dicts
            
        Returns:
            List of document IDs
        """
        try:
            points = []
            doc_ids = []
            
            for text, embedding, meta in zip(texts, embeddings, metadata):
                doc_id = str(uuid.uuid4())
                doc_ids.append(doc_id)
                
                # Add text and timestamp to metadata
                meta['text'] = text
                meta['timestamp'] = datetime.utcnow().isoformat()
                
                point = PointStruct(
                    id=doc_id,
                    vector=embedding,
                    payload=meta
                )
                points.append(point)
            
            # Upload to Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            
            logger.info(f"Added {len(points)} documents to vector store")
            return doc_ids
            
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {e}")
            raise
    
    async def search(
        self,
        query_embedding: List[float],
        top_k: int = None,
        filter_dict: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Search for similar documents
        
        Args:
            query_embedding: Query embedding vector
            top_k: Number of results to return
            filter_dict: Optional metadata filters
            
        Returns:
            List of search results with text and metadata
        """
        try:
            if top_k is None:
                top_k = settings.TOP_K_RESULTS
            
            # Build filter if provided
            search_filter = None
            if filter_dict:
                conditions = []
                for key, value in filter_dict.items():
                    conditions.append(
                        FieldCondition(
                            key=key,
                            match=MatchValue(value=value)
                        )
                    )
                search_filter = Filter(must=conditions)
            
            # Perform search
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k,
                query_filter=search_filter
            )
            
            # Format results
            results = []
            for result in search_results:
                results.append({
                    'id': result.id,
                    'score': result.score,
                    'text': result.payload.get('text', ''),
                    'metadata': {k: v for k, v in result.payload.items() if k != 'text'}
                })
            
            logger.info(f"Found {len(results)} similar documents")
            return results
            
        except Exception as e:
            logger.error(f"Error searching vector store: {e}")
            raise
    
    async def delete_by_filename(self, filename: str) -> bool:
        """
        Delete all documents with specific filename
        
        Args:
            filename: Filename to delete
            
        Returns:
            Success status
        """
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=Filter(
                    must=[
                        FieldCondition(
                            key="filename",
                            match=MatchValue(value=filename)
                        )
                    ]
                )
            )
            logger.info(f"Deleted documents with filename: {filename}")
            return True
        except Exception as e:
            logger.error(f"Error deleting documents: {e}")
            return False
    
    def get_collection_info(self) -> Dict:
        """
        Get collection statistics
        
        Returns:
            Collection info dict
        """
        try:
            collection_info = self.client.get_collection(self.collection_name)
            return {
                'name': self.collection_name,
                'points_count': collection_info.points_count,
                'status': collection_info.status
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return {}

# Create global instance
vector_store = VectorStore()