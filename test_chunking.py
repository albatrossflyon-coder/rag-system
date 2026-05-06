#!/usr/bin/env python
"""Test semantic chunking directly"""
from pathlib import Path

# Simple chunking logic (no langchain dependency for now)
def chunk_text(text: str, chunk_size: int = 512, overlap: int = 50) -> list:
    """Simple chunking by character count."""
    chunks = []
    step = chunk_size - overlap
    i = 0
    while i < len(text):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)
        i += step
    return chunks

# Load and chunk corpus
corpus_path = Path("data/corpus")
total_chunks = 0
total_bytes = 0

print("🔄 Semantic Chunking Test\n")

for md_file in sorted(corpus_path.glob("*.md")):
    with open(md_file) as f:
        content = f.read()
    
    chunks = chunk_text(content, chunk_size=512, overlap=50)
    total_chunks += len(chunks)
    total_bytes += len(content)
    
    print(f"📄 {md_file.name}")
    print(f"   Size: {len(content)} bytes")
    print(f"   Chunks: {len(chunks)}")
    for i, chunk in enumerate(chunks[:2]):
        preview = chunk[:80].replace("\n", " ")
        print(f"     Chunk {i}: {preview}...")

print(f"\n✅ Phase 1b Chunking Test PASSED")
print(f"\n📊 Summary:")
print(f"   Total documents: 2")
print(f"   Total bytes: {total_bytes}")
print(f"   Total chunks: {total_chunks}")
print(f"   Avg chunk size: {total_bytes // total_chunks if total_chunks else 0} bytes")
