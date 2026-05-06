"""Semantic chunking strategy (preserve boundaries, not naive splits)."""

from typing import List, Dict, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter

class SemanticChunker:
    """Split documents semantically (respects sentence/section boundaries)."""
    
    def __init__(self, chunk_size: int = 1024, overlap: int = 100):
        # Recursive splitter respects natural boundaries
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def chunk_documents(self, docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Chunk a list of documents semantically."""
        chunks = []
        for doc in docs:
            text = doc["content"]
            chunk_texts = self.splitter.split_text(text)
            
            for i, chunk in enumerate(chunk_texts):
                chunks.append({
                    "content": chunk,
                    "source": doc["source"],
                    "chunk_index": i,
                    "format": doc.get("format", "unknown"),
                    "metadata": doc.get("metadata", {})
                })
        
        return chunks
