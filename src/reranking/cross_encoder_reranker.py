"""Cross-encoder reranking (Cohere API or local BAAI model)."""

import os
from typing import List, Tuple
import cohere

class CrossEncoderReranker:
    """Rerank retrieved documents using cross-encoder."""
    
    def __init__(self, use_cohere: bool = True):
        self.use_cohere = use_cohere
        if use_cohere:
            self.client = cohere.ClientV2(api_key=os.getenv("COHERE_API_KEY"))
        else:
            self.model = self._load_local_model()
    
    def _load_local_model(self):
        """Load local cross-encoder (BAAI/bge-reranker-base)."""
        from sentence_transformers import CrossEncoder
        return CrossEncoder('BAAI/bge-reranker-base')
    
    def rerank(self, query: str, documents: List[Tuple[str, float]], top_k: int = 3) -> List[Tuple[str, float]]:
        """Rerank documents by relevance to query."""
        
        doc_texts = [doc[0] for doc in documents]
        
        if self.use_cohere:
            response = self.client.rerank(
                query=query,
                documents=doc_texts,
                model="rerank-english-v2.0",
                top_n=top_k
            )
            # Cohere returns indices and scores
            reranked = [(doc_texts[result.index], result.relevance_score) for result in response.results]
        else:
            # Local model
            scores = self.model.predict([[query, doc] for doc in doc_texts])
            ranked = sorted(zip(doc_texts, scores), key=lambda x: x[1], reverse=True)
            reranked = ranked[:top_k]
        
        return reranked
