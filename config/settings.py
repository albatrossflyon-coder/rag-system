from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Keys
    anthropic_api_key: str
    pinecone_api_key: str
    cohere_api_key: Optional[str] = None
    
    # Pinecone Config
    pinecone_index: str = "rag-production"
    pinecone_environment: str = "us-west-2"
    
    # Deployment
    deployment_env: str = "local"
    frontend_url: str = "http://localhost:3000"
    api_port: int = 8000
    
    # Evaluation Thresholds
    eval_threshold_faithfulness: float = 0.75
    eval_threshold_relevance: float = 0.80
    eval_batch_size: int = 10
    
    # Retrieval Config
    retrieval_top_k: int = 5  # BM25 + vector candidates
    rerank_top_k: int = 3     # After reranking
    
    # Chunking Config
    chunk_max_tokens: int = 1024
    chunk_overlap: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
