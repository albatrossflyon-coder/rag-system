#!/usr/bin/env python
"""Quick test - just load corpus, no dependencies"""
import os
from pathlib import Path

corpus_path = Path("data/corpus")
print(f"Corpus path: {corpus_path}")
print(f"Exists: {corpus_path.exists()}")

if corpus_path.exists():
    md_files = list(corpus_path.glob("*.md"))
    print(f"\n✅ Found {len(md_files)} markdown files:")
    for md_file in md_files:
        size = os.path.getsize(md_file)
        print(f"  - {md_file.name}: {size} bytes")
        
        # Read and display first 200 chars
        with open(md_file) as f:
            content = f.read()
            preview = content[:200].replace("\n", " ")
            print(f"    Preview: {preview}...")
else:
    print("❌ Corpus path not found")
