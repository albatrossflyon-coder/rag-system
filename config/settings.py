import os
from pathlib import Path
from typing import Optional

try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
except ImportError:  # pragma: no cover - optional runtime dependency
    BaseSettings = None
    SettingsConfigDict = None

BASE_DIR = Path(__file__).resolve().parents[1]

if BaseSettings is not None:
    class Settings(BaseSettings):
        # API Keys
        anthropic_api_key: Optional[str] = None
        pinecone_api_key: Optional[str] = None
        cohere_api_key: Optional[str] = None

        # Pinecone Config
        pinecone_index: str = "rag-production"
        pinecone_environment: str = "us-west-2"

        # Deployment
        deployment_env: str = "local"
        frontend_url: str = "http://localhost:3000"
        api_port: int = 8000

        # Corpus
        corpus_path: Path = BASE_DIR / "data" / "corpus"

        # Evaluation Thresholds
        eval_threshold_faithfulness: float = 0.75
        eval_threshold_relevance: float = 0.80
        eval_batch_size: int = 10

        # Retrieval Config
        retrieval_top_k: int = 5
        rerank_top_k: int = 3

        # Chunking Config
        chunk_max_tokens: int = 1024
        chunk_overlap: int = 100

        model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", case_sensitive=False)
else:
    def _read_env_file() -> dict[str, str]:
        env_file = BASE_DIR / ".env"
        values: dict[str, str] = {}
        if not env_file.exists():
            return values
        for raw_line in env_file.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip()
        return values


    class Settings:
        def __init__(self):
            env_values = _read_env_file()

            def get_value(name: str, default, cast=None):
                raw = os.getenv(name)
                if raw is None:
                    raw = env_values.get(name)
                if raw is None:
                    return default
                return cast(raw) if cast else raw

            self.anthropic_api_key: Optional[str] = get_value("ANTHROPIC_API_KEY", None)
            self.pinecone_api_key: Optional[str] = get_value("PINECONE_API_KEY", None)
            self.cohere_api_key: Optional[str] = get_value("COHERE_API_KEY", None)

            self.pinecone_index: str = get_value("PINECONE_INDEX", "rag-production")
            self.pinecone_environment: str = get_value("PINECONE_ENVIRONMENT", "us-west-2")

            self.deployment_env: str = get_value("DEPLOYMENT_ENV", "local")
            self.frontend_url: str = get_value("FRONTEND_URL", "http://localhost:3000")
            self.api_port: int = get_value("API_PORT", 8000, int)

            self.corpus_path: Path = Path(get_value("CORPUS_PATH", str(BASE_DIR / "data" / "corpus"))).resolve()

            self.eval_threshold_faithfulness: float = get_value("EVAL_THRESHOLD_FAITHFULNESS", 0.75, float)
            self.eval_threshold_relevance: float = get_value("EVAL_THRESHOLD_RELEVANCE", 0.80, float)
            self.eval_batch_size: int = get_value("RAGAS_BATCH_SIZE", 10, int)

            self.retrieval_top_k: int = get_value("RETRIEVAL_TOP_K", 5, int)
            self.rerank_top_k: int = get_value("RERANK_TOP_K", 3, int)
            self.chunk_max_tokens: int = get_value("CHUNK_MAX_TOKENS", 1024, int)
            self.chunk_overlap: int = get_value("CHUNK_OVERLAP", 100, int)


settings = Settings()
