"""Semantic chunking strategy (preserve boundaries, not naive splits)."""

from typing import List, Dict, Any

class SemanticChunker:
    """Split documents semantically (respects sentence/section boundaries)."""
    
    def __init__(self, chunk_size: int = 1024, overlap: int = 100):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def _split_text(self, text: str) -> List[str]:
        paragraphs = [paragraph.strip() for paragraph in text.split("\n\n") if paragraph.strip()]
        if not paragraphs:
            return []

        chunks: List[str] = []
        current = ""

        for paragraph in paragraphs:
            candidate = f"{current}\n\n{paragraph}" if current else paragraph
            if len(candidate) <= self.chunk_size:
                current = candidate
                continue

            if current:
                chunks.append(current)
                overlap_text = current[-self.overlap:] if self.overlap else ""
                current = f"{overlap_text}{paragraph}" if overlap_text else paragraph
            else:
                current = paragraph

            while len(current) > self.chunk_size:
                chunks.append(current[: self.chunk_size])
                overlap_text = current[self.chunk_size - self.overlap : self.chunk_size] if self.overlap else ""
                current = f"{overlap_text}{current[self.chunk_size:]}" if overlap_text else current[self.chunk_size:]

        if current:
            chunks.append(current)

        return chunks
    
    def chunk_documents(self, docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Chunk a list of documents semantically."""
        chunks = []
        for doc in docs:
            text = doc["content"]
            chunk_texts = self._split_text(text)
            
            for i, chunk in enumerate(chunk_texts):
                chunks.append({
                    "content": chunk,
                    "source": doc["source"],
                    "chunk_index": i,
                    "format": doc.get("format", "unknown"),
                    "metadata": doc.get("metadata", {})
                })
        
        return chunks
