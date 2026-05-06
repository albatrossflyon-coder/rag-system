#!/usr/bin/env python
"""Test ingestion pipeline Phase 1b"""
from src.ingestion import CorpusLoader, SemanticChunker

# Load corpus
print("Loading corpus...")
loader = CorpusLoader()
docs = loader.load_all()
print(f"✅ Loaded {len(docs)} documents")
for doc in docs:
    source = doc.get("source", "unknown")
    content_len = len(doc.get("content", ""))
    print(f"  - {source}: {content_len} chars")

# Chunk semantically
print("\nChunking semantically...")
chunker = SemanticChunker(chunk_size=512, overlap=50)
chunks = chunker.chunk_documents(docs)
print(f"✅ Created {len(chunks)} semantic chunks")
for i, chunk in enumerate(chunks[:5]):
    source = chunk.get("source", "unknown")
    chunk_idx = chunk.get("chunk_index", "?")
    content_len = len(chunk.get("content", ""))
    print(f"  - {source} chunk {chunk_idx}: {content_len} chars")

print("\n✅ Phase 1b ingestion test PASSED")
print(f"\nSummary:")
print(f"  Docs: {len(docs)}")
print(f"  Total chunks: {len(chunks)}")
print(f"  Avg chunk size: {sum(len(c.get('content', '')) for c in chunks) // len(chunks) if chunks else 0} chars")
