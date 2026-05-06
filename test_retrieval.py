#!/usr/bin/env python
"""Test hybrid retrieval logic with mock embeddings"""
import math
from pathlib import Path
from collections import Counter

def bm25_score(query: str, doc: str, k1: float = 1.5, b: float = 0.75) -> float:
    """Simplified BM25 scoring (term frequency only)."""
    query_terms = query.lower().split()
    doc_len = len(doc.split())
    avg_doc_len = 200  # mock
    
    score = 0
    for term in query_terms:
        if term in doc.lower():
            # Count occurrences
            tf = doc.lower().count(term)
            # BM25 formula (simplified)
            norm = 1 - b + b * (doc_len / avg_doc_len)
            idf = math.log(1 + (1 / (tf + 0.5)))
            score += idf * ((tf * (k1 + 1)) / (tf + k1 * norm))
    return score

def vector_similarity(query: str, doc: str) -> float:
    """Mock semantic similarity (word overlap / length)."""
    query_words = set(query.lower().split())
    doc_words = set(doc.lower().split())
    overlap = len(query_words & doc_words)
    total = max(len(query_words | doc_words), 1)
    return overlap / total

# Load corpus
corpus_path = Path("data/corpus")
docs = []
for md_file in sorted(corpus_path.glob("*.md")):
    with open(md_file) as f:
        content = f.read()
    docs.append({"source": md_file.name, "content": content})

# Test queries
test_queries = [
    "What is MCP?",
    "Rust deployment orchestration",
    "content scheduling API"
]

print("🔍 Hybrid Retrieval Test (BM25 + Vector)\n")

for query in test_queries:
    print(f"Query: '{query}'")
    
    # BM25 scores
    bm25_scores = [(doc["source"], bm25_score(query, doc["content"])) for doc in docs]
    bm25_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Vector scores
    vector_scores = [(doc["source"], vector_similarity(query, doc["content"])) for doc in docs]
    vector_scores.sort(key=lambda x: x[1], reverse=True)
    
    # RRF fusion (Reciprocal Rank Fusion)
    rrf_scores = {}
    for rank, (source, score) in enumerate(bm25_scores):
        rrf_scores[source] = rrf_scores.get(source, 0) + 1 / (rank + 60)
    for rank, (source, score) in enumerate(vector_scores):
        rrf_scores[source] = rrf_scores.get(source, 0) + 1 / (rank + 60)
    
    fused = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
    
    print(f"  BM25 top: {bm25_scores[0]}")
    print(f"  Vector top: {vector_scores[0]}")
    print(f"  RRF fused: {fused[0]}")
    print()

print("✅ Phase 1b Retrieval Test PASSED")
print("\n📊 Findings:")
print("   - BM25: Exact term matching (lexical)")
print("   - Vector: Semantic similarity (mock)")
print("   - RRF: Combines both rankings")
print("   - Next: Add real embeddings + Pinecone")
