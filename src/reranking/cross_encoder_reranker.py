"""Rerank retrieved documents using Cohere when available or a local relevance heuristic."""

import os
import re
from typing import Any, Dict, List

try:
    import cohere
except ImportError:  # pragma: no cover - depends on optional package
    cohere = None

TOKEN_RE = re.compile(r"[A-Za-z0-9_]+")


class CrossEncoderReranker:
    """Rerank retrieved documents while preserving source metadata."""

    def __init__(self, use_cohere: bool = True):
        self.use_cohere = use_cohere and cohere is not None
        self.client = cohere.ClientV2(api_key=os.getenv("COHERE_API_KEY")) if self.use_cohere else None

    @staticmethod
    def _tokenize(text: str) -> set[str]:
        return set(TOKEN_RE.findall(text.lower()))

    def _local_score(self, query: str, document: Dict[str, Any]) -> float:
        query_terms = self._tokenize(query)
        document_terms = self._tokenize(document["content"])
        if not query_terms:
            return float(document.get("fusion_score", 0.0))

        overlap = len(query_terms & document_terms) / len(query_terms)
        return (overlap * 0.85) + (float(document.get("fusion_score", 0.0)) * 0.15)

    def rerank(self, query: str, documents: List[Dict[str, Any]], top_k: int = 3) -> List[Dict[str, Any]]:
        """Rerank documents by query relevance and keep source metadata intact."""
        if not documents:
            return []

        limit = min(top_k, len(documents))

        if self.use_cohere and self.client is not None:
            response = self.client.rerank(
                query=query,
                documents=[document["content"] for document in documents],
                model="rerank-english-v2.0",
                top_n=limit,
            )
            reranked: List[Dict[str, Any]] = []
            for result in response.results:
                document = dict(documents[result.index])
                document["rerank_score"] = result.relevance_score
                reranked.append(document)
            return reranked

        reranked = []
        for document in documents:
            updated = dict(document)
            updated["rerank_score"] = self._local_score(query, document)
            reranked.append(updated)

        reranked.sort(key=lambda document: document["rerank_score"], reverse=True)
        return reranked[:limit]
