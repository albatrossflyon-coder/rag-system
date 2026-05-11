"""Hybrid retrieval: lexical BM25-style scoring + local vector similarity with RRF."""

import math
import re
from collections import Counter
from typing import Any, Dict, List

TOKEN_RE = re.compile(r"[A-Za-z0-9_]+")


class HybridRetriever:
    """Combine lexical BM25-style retrieval with local TF-IDF vector similarity."""

    def __init__(self, top_k: int = 5, use_pinecone: bool = False):
        self.top_k = top_k
        self.use_pinecone = use_pinecone
        self.documents: List[Dict[str, Any]] = []
        self.doc_term_counts: List[Counter[str]] = []
        self.doc_lengths: List[int] = []
        self.term_idf: Dict[str, float] = {}
        self.document_vectors: List[Dict[str, float]] = []
        self.avg_doc_length = 0.0
        self.k1 = 1.5
        self.b = 0.75

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        return TOKEN_RE.findall(text.lower())

    def index_documents(self, documents: List[Dict[str, Any]]) -> None:
        """Index chunked documents for hybrid retrieval."""
        if self.use_pinecone:
            raise NotImplementedError("Pinecone indexing is not wired for the local Phase 1b corpus run.")
        if not documents:
            raise ValueError("No documents were provided for indexing.")

        self.documents = [dict(doc) for doc in documents]
        self.doc_term_counts = [Counter(self._tokenize(doc["content"])) for doc in self.documents]
        self.doc_lengths = [sum(term_counts.values()) or 1 for term_counts in self.doc_term_counts]
        self.avg_doc_length = sum(self.doc_lengths) / len(self.doc_lengths)

        doc_freqs: Counter[str] = Counter()
        for term_counts in self.doc_term_counts:
            doc_freqs.update(term_counts.keys())

        doc_count = len(self.documents)
        self.term_idf = {
            term: math.log(((doc_count - freq + 0.5) / (freq + 0.5)) + 1.0)
            for term, freq in doc_freqs.items()
        }

        self.document_vectors = [self._tfidf_vector(term_counts) for term_counts in self.doc_term_counts]

    def _tfidf_vector(self, term_counts: Counter[str]) -> Dict[str, float]:
        vector: Dict[str, float] = {}
        total_terms = sum(term_counts.values()) or 1

        for term, count in term_counts.items():
            idf = self.term_idf.get(term)
            if idf is None:
                continue
            vector[term] = (count / total_terms) * idf

        norm = math.sqrt(sum(weight * weight for weight in vector.values()))
        if norm == 0:
            return vector
        return {term: weight / norm for term, weight in vector.items()}

    @staticmethod
    def _cosine_similarity(left: Dict[str, float], right: Dict[str, float]) -> float:
        if not left or not right:
            return 0.0
        return sum(weight * right.get(term, 0.0) for term, weight in left.items())

    def _bm25_score(self, query_terms: List[str], doc_index: int) -> float:
        term_counts = self.doc_term_counts[doc_index]
        doc_length = self.doc_lengths[doc_index]
        score = 0.0

        for term in query_terms:
            tf = term_counts.get(term, 0)
            if tf == 0:
                continue
            idf = self.term_idf.get(term, 0.0)
            norm = 1 - self.b + self.b * (doc_length / max(self.avg_doc_length, 1.0))
            score += idf * ((tf * (self.k1 + 1)) / (tf + self.k1 * norm))

        return score

    def retrieve_hybrid(self, query: str) -> List[Dict[str, Any]]:
        """Retrieve with BM25-style sparse scoring + TF-IDF cosine similarity + RRF."""
        if not self.documents:
            raise RuntimeError("Retriever has not been indexed yet. Load and index the corpus first.")
        if not query or not query.strip():
            raise ValueError("Query cannot be empty.")

        query_terms = self._tokenize(query)
        query_vector = self._tfidf_vector(Counter(query_terms))

        sparse_scores = [self._bm25_score(query_terms, index) for index in range(len(self.documents))]
        dense_scores = [self._cosine_similarity(doc_vector, query_vector) for doc_vector in self.document_vectors]

        sparse_ranking = sorted(range(len(self.documents)), key=lambda index: sparse_scores[index], reverse=True)
        dense_ranking = sorted(range(len(self.documents)), key=lambda index: dense_scores[index], reverse=True)

        rrf_scores: Dict[int, float] = {}
        window = max(self.top_k * 2, len(self.documents))
        for rank, index in enumerate(sparse_ranking[:window]):
            rrf_scores[index] = rrf_scores.get(index, 0.0) + 1 / (rank + 60)
        for rank, index in enumerate(dense_ranking[:window]):
            rrf_scores[index] = rrf_scores.get(index, 0.0) + 1 / (rank + 60)

        fused_indices = sorted(rrf_scores, key=lambda index: rrf_scores[index], reverse=True)[: self.top_k]

        results: List[Dict[str, Any]] = []
        for index in fused_indices:
            result = dict(self.documents[index])
            result["sparse_score"] = sparse_scores[index]
            result["dense_score"] = dense_scores[index]
            result["fusion_score"] = rrf_scores[index]
            results.append(result)

        return results
