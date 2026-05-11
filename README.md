# RAG System — Production-Grade "Ask My Docs"

**Phase 1 Complete:** Domain-agnostic architecture with hybrid retrieval, reranking, evaluation, and observability.

**Phase 1b in progress:** the local corpus now bootstraps into an in-memory hybrid index on startup so the sample corpus can be exercised end-to-end before cloud deployment.

## Architecture

```
Query → Retrieval (BM25 + Vector) → Reranking (Cross-Encoder) → Generation (Claude) → Sources
                ↓
          Evaluation (Ragas metrics)
```

**Key Features:**
- ✅ Hybrid search (sparse + dense)
- ✅ Cross-encoder reranking
- ✅ Semantic chunking (not naive splits)
- ✅ Ragas evaluation (faithfulness, relevance, precision)
- ✅ Structured logging for observability
- ✅ FastAPI with CORS for Vercel frontend

## Quick Start

### 1. Setup
```bash
cd rag-system
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure
```bash
cp .env.example .env
# Fill in ANTHROPIC_API_KEY for live answer generation.
# Cohere and Pinecone are optional for the local corpus run.
```

### 3. Load Corpus
Add markdown or JSON files to `data/corpus/`:
```bash
echo "# Test Doc\nThis is test content." > data/corpus/test.md
```

### 4. Run API
```bash
cd api
python main.py
# Server runs on http://localhost:8000
```

### 5. Test
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "What is in the corpus?"}'
```

### 6. Run the local pipeline checks
```bash
python -m unittest discover -s tests -p "test_*.py"
```

### 7. Query the local corpus without the API server
```bash
python query_local.py "What is MCP?"

# Generate a final answer too (requires ANTHROPIC_API_KEY)
python query_local.py "What is MCP?" --answer
```

## Project Structure

```
rag-system/
├── api/
│   └── main.py              # FastAPI server
├── config/
│   └── settings.py          # Pydantic settings
├── src/
│   ├── ingestion/           # Corpus loading + semantic chunking
│   ├── retrieval/           # BM25 + vector (RRF fusion)
│   ├── reranking/           # Cross-encoder reranking
│   ├── generation/          # Claude answer generation
│   └── evaluation/          # Ragas metrics
├── data/
│   ├── corpus/              # Your documents (markdown, JSON)
│   └── vectors/             # Chroma vector store (local dev)
├── tests/                   # Unit & integration tests
├── notebooks/               # Jupyter exploration
├── requirements.txt         # Dependencies
└── .env.example             # Configuration template
```

## Metrics (Phase 1)

### Faithfulness
- Does the generated answer come from context?
- Target: ≥ 0.75

### Answer Relevancy
- Does the answer address the question?
- Target: ≥ 0.80

### Context Precision
- Are retrieved documents relevant?
- Bonus: Helps debug retrieval pipeline

## What's NOT in Phase 1

- Stripe/payment (Phase 2)
- YouTube API integration (Phase 2)
- Auth/login (local only)
- Vercel frontend (separate repo)
- Production Pinecone setup (use local Chroma for dev)

## Next Steps

1. **Phase 1b:** Load real corpus, test end-to-end
2. **Phase 2:** Cloud deployment (Railway backend, Vercel frontend)
3. **Phase 3:** Observability dashboard + evaluation metrics
4. **Phase 4:** Add Vercel, Railway tokens; deploy live

## References

- [LangChain RAG](https://docs.langchain.com/oss/python/langchain/rag)
- [Ragas Evaluation](https://docs.ragas.io/)
- [FastAPI](https://fastapi.tiangolo.com/)
