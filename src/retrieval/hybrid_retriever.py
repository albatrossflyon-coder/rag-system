"""Hybrid retrieval: BM25 + vector search with reciprocal rank fusion."""

import os
from typing import List, Dict, Any, Tuple
from langchain.retrievers import BM25Retriever
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.retrievers import PineconeHybridSearchRetriever
import numpy as np

class HybridRetriever:
    """Combine BM25 (sparse) + vector search (dense) with RRF fusion."""
    
    def __init__(self, top_k: int = 5, use_pinecone: bool = False):
        self.top_k = top_k
        self.use_pinecone = use_pinecone
        self.embeddings = OpenAIEmbeddings()
        
        if use_pinecone:
            self.vector_store = self._init_pinecone()
        else:
            self.vector_store = self._init_chroma()
        
        self.bm25_retriever = None  # Initialized after ingestion
    
    def _init_chroma(self) -> Chroma:
        """Local Chroma vector store (dev)."""
        return Chroma(
            collection_name="rag-corpus",
            embedding_function=self.embeddings,
            persist_directory="data/vectors"
        )
    
    def _init_pinecone(self):
        """Pinecone cloud vector store (prod)."""
        from pinecone import Pinecone
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        return pc.Index("rag-production")
    
    def set_bm25_retriever(self, documents: List[Dict[str, Any]]):
        """Initialize BM25 retriever with documents."""
        # Format for BM25
        docs_text = [doc["content"] for doc in documents]
        self.bm25_retriever = BM25Retriever.from_texts(docs_text)
    
    def retrieve_hybrid(self, query: str) -> List[Tuple[str, float]]:
        """Retrieve using BM25 + vector, fuse with RRF."""
        
        # BM25 retrieval
        bm25_results = self.bm25_retriever.get_relevant_documents(query)[:self.top_k]
        bm25_dict = {doc.page_content: i for i, doc in enumerate(bm25_results)}
        
        # Vector retrieval
        vector_results = self.vector_store.similarity_search_with_score(query, k=self.top_k)
        vector_dict = {doc[0].page_content: i for i, doc in enumerate(vector_results)}
        
        # Reciprocal Rank Fusion (RRF)
        rrf_scores = {}
        for content, rank in bm25_dict.items():
            rrf_scores[content] = rrf_scores.get(content, 0) + 1 / (rank + 60)
        for content, rank in vector_dict.items():
            rrf_scores[content] = rrf_scores.get(content, 0) + 1 / (rank + 60)
        
        # Sort by RRF score
        ranked = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
        return ranked[:self.top_k]
