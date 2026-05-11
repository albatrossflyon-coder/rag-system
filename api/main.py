"""FastAPI RAG endpoint."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.ingestion import CorpusLoader, SemanticChunker
from src.pipeline import bootstrap_corpus as bootstrap_local_corpus, new_pipeline_state
from src.retrieval import HybridRetriever
from src.reranking import CrossEncoderReranker
from src.generation import ClaudeGenerator
from config.settings import settings

# Initialize components
loader = CorpusLoader(corpus_path=settings.corpus_path)
chunker = SemanticChunker(chunk_size=settings.chunk_max_tokens, overlap=settings.chunk_overlap)
retriever = HybridRetriever(top_k=settings.retrieval_top_k, use_pinecone=settings.deployment_env == "production")
reranker = CrossEncoderReranker(use_cohere=bool(settings.cohere_api_key))
generator = ClaudeGenerator()
pipeline_state = new_pipeline_state()

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
    top_k: Optional[int] = None

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: str

def bootstrap_corpus() -> None:
    """Load, chunk, and index the local corpus for retrieval."""
    bootstrap_local_corpus(loader, chunker, retriever, settings.corpus_path, pipeline_state)


@app.on_event("startup")
async def startup_event():
    bootstrap_corpus()


@app.post("/ask", response_model=QueryResponse)
async def ask(request: QueryRequest):
    """Ask a question; return grounded answer + sources."""
    try:
        if not pipeline_state["ready"]:
            bootstrap_corpus()

        # Retrieve
        results = retriever.retrieve_hybrid(request.query)

        # Rerank
        rerank_limit = request.top_k or settings.rerank_top_k
        reranked = reranker.rerank(request.query, results, top_k=rerank_limit)

        # Generate
        response = generator.generate(request.query, reranked)

        return QueryResponse(
            answer=response["answer"],
            sources=response["sources"],
            confidence=response["confidence"]
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    """Health check."""
    return {
        "status": "ok" if pipeline_state["ready"] else "initializing",
        "documents": pipeline_state["documents"],
        "chunks": pipeline_state["chunks"],
        "sources": pipeline_state["sources"],
    }

@app.get("/metrics")
async def metrics():
    """Return evaluation metrics."""
    return {
        "faithfulness_threshold": settings.eval_threshold_faithfulness,
        "relevance_threshold": settings.eval_threshold_relevance,
        "deployment_env": settings.deployment_env,
        "documents": pipeline_state["documents"],
        "chunks": pipeline_state["chunks"],
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.api_port)
