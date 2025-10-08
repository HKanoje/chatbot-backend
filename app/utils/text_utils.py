# app/utils/text_utils.py
from typing import List
import re

def clean_text(text: str) -> str:
    """
    Clean and normalize text
    
    Args:
        text: Raw text
        
    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep punctuation
    text = re.sub(r'[^\w\s.,!?;:()\-\']', '', text)
    return text.strip()

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Split text into overlapping chunks
    
    Args:
        text: Text to chunk
        chunk_size: Maximum chunk size in characters
        overlap: Overlap between chunks
        
    Returns:
        List of text chunks
    """
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # Try to break at sentence boundary
        if end < len(text):
            # Look for sentence end within last 100 chars of chunk
            last_period = text.rfind('.', end - 100, end)
            last_question = text.rfind('?', end - 100, end)
            last_exclamation = text.rfind('!', end - 100, end)
            
            break_point = max(last_period, last_question, last_exclamation)
            if break_point > start:
                end = break_point + 1
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        start = end - overlap
    
    return chunks

def extract_keywords(text: str, top_n: int = 5) -> List[str]:
    """
    Extract simple keywords from text (basic implementation)
    
    Args:
        text: Input text
        top_n: Number of keywords to extract
        
    Returns:
        List of keywords
    """
    # Simple keyword extraction (you can enhance this)
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    
    # Remove common stop words
    stop_words = {'this', 'that', 'with', 'from', 'have', 'been', 'were', 'will', 'would', 'could', 'should'}
    words = [w for w in words if w not in stop_words]
    
    # Count frequency
    word_freq = {}
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    # Sort by frequency and return top N
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, freq in sorted_words[:top_n]]