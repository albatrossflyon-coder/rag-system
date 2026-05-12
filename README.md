# Grounded RAG System

A production-grade retrieval-augmented generation architecture built to eliminate hallucinations and provide grounded, source-cited answers from private document corpora.

**Stack:** FastAPI · LangChain · Claude API · Chroma (local) / Pinecone (cloud) · Ragas evaluation

---

## The Problem It Solves

Stock LLMs hallucinate. When you need an AI to answer questions from *your* documents — contracts, specs, internal knowledge bases — you can't afford wrong answers. This system retrieves the exact source passages, reranks them by relevance, generates an answer grounded only in that context, and scores itself for faithfulness before returning a response.

## Architecture

```
Query
  → Hybrid Retrieval (BM25 sparse + dense vector, RRF fusion)
  → Cross-Encoder Reranking
  → Claude Generation (grounded to retrieved context only)
  → Ragas Evaluation (faithfulness, relevance, context precision)
  → Response + Source Citations
```

**Key design decisions:**
- **Hybrid search over vector-only** — BM25 catches exact keyword matches that dense vectors miss (product codes, names, technical terms)
- **Cross-encoder reranking** — bi-encoder retrieval is fast but imprecise; the reranker re-scores the top-k candidates with full query-passage attention
- **Semantic chunking over naive splits** — preserves paragraph/section context instead of cutting mid-sentence
- **Ragas evaluation in the response loop** — catches low-confidence answers before they reach the user

## Features

- Hybrid search (sparse BM25 + dense vector with RRF fusion)
- Cross-encoder reranking for precision
- Semantic chunking (not naive character splits)
- Claude-powered answer generation grounded to retrieved context
- Ragas evaluation metrics: faithfulness ≥ 0.75, relevance ≥ 0.80
- FastAPI server with CORS for frontend integration
- Structured logging for observability

## Quick Start

```bash
git clone https://github.com/albatrossflyon-coder/rag-system
cd rag-system
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # Add your ANTHROPIC_API_KEY
```

Drop your documents (markdown or JSON) into `data/corpus/`, then:

```bash
# Start the API server
cd api && python main.py

# Ask a question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "What does the contract say about payment terms?"}'

# Query without the server (local pipeline)
python query_local.py "What is MCP?" --answer

# Run the test suite
python -m unittest discover -s tests -p "test_*.py"
```

## Project Structure

```
rag-system/
├── api/
│   └── main.py              # FastAPI server — /ask endpoint
├── src/
│   ├── ingestion/           # Document loading + semantic chunking
│   ├── retrieval/           # BM25 + vector hybrid search (RRF)
│   ├── reranking/           # Cross-encoder reranking
│   ├── generation/          # Claude answer generation
│   └── evaluation/          # Ragas faithfulness + relevance scoring
├── config/
│   └── settings.py          # Pydantic settings
├── data/
│   ├── corpus/              # Your documents go here
│   └── vectors/             # Chroma vector store (local dev)
├── tests/                   # Unit + integration tests
├── query_local.py           # CLI query tool (no server needed)
└── .env.example             # Configuration template
```

## Evaluation Targets

| Metric | Target | What it measures |
|--------|--------|-----------------|
| Faithfulness | ≥ 0.75 | Answer comes from retrieved context, not hallucination |
| Answer Relevancy | ≥ 0.80 | Answer actually addresses the question |
| Context Precision | Tracked | Retrieved chunks are relevant to the query |

## Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | Claude answer generation |
| `PINECONE_API_KEY` | No | Cloud vector store (uses local Chroma if omitted) |
| `COHERE_API_KEY` | No | Cohere reranker (uses local cross-encoder if omitted) |

## Built By

[Chris Brown](https://albatrossai.online) — AI Infrastructure Lead  
[github.com/albatrossflyon-coder](https://github.com/albatrossflyon-coder)
