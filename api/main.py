"""FastAPI RAG endpoint."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.ingestion import CorpusLoader, SemanticChunker
from src.retrieval import HybridRetriever
from src.reranking import CrossEncoderReranker
from src.generation import ClaudeGenerator
from src.evaluation import RagasEvaluator
from config.settings import settings

# Initialize components
loader = CorpusLoader()
chunker = SemanticChunker(chunk_size=settings.chunk_max_tokens, overlap=settings.chunk_overlap)
retriever = HybridRetriever(top_k=settings.retrieval_top_k, use_pinecone=settings.deployment_env == "production")
reranker = CrossEncoderReranker(use_cohere=bool(settings.cohere_api_key))
generator = ClaudeGenerator()
evaluator = RagasEvaluator(
    faithfulness_threshold=settings.eval_threshold_faithfulness,
    relevance_threshold=settings.eval_threshold_relevance
)

app = FastAPI(title="RAG System", version="0.1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 3

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: str

@app.post("/ask", response_model=QueryResponse)
async def ask(request: QueryRequest):
    """Ask a question; return grounded answer + sources."""
    
    try:
        # Retrieve
        results = retriever.retrieve_hybrid(request.query)
        
        # Rerank
        reranked = reranker.rerank(request.query, results, top_k=request.top_k)
        
        # Generate
        response = generator.generate(request.query, reranked)
        
        return QueryResponse(
            answer=response["answer"],
            sources=response["sources"],
            confidence=response["confidence"]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    """Health check."""
    return {"status": "ok"}

@app.get("/metrics")
async def metrics():
    """Return evaluation metrics."""
    return {
        "faithfulness_threshold": settings.eval_threshold_faithfulness,
        "relevance_threshold": settings.eval_threshold_relevance,
        "deployment_env": settings.deployment_env
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.api_port)
