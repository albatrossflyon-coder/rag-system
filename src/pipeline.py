from pathlib import Path
from typing import Any, Dict


def new_pipeline_state() -> Dict[str, Any]:
    return {
        "ready": False,
        "documents": 0,
        "chunks": 0,
        "sources": [],
    }


def bootstrap_corpus(loader, chunker, retriever, corpus_path: Path, state: Dict[str, Any] | None = None) -> Dict[str, Any]:
    docs = loader.load_all()
    if not docs:
        raise RuntimeError(f"No corpus documents were found in '{corpus_path}'.")

    chunks = chunker.chunk_documents(docs)
    if not chunks:
        raise RuntimeError("Corpus loaded successfully but produced no chunks.")

    retriever.index_documents(chunks)

    if state is None:
        state = new_pipeline_state()

    state["ready"] = True
    state["documents"] = len(docs)
    state["chunks"] = len(chunks)
    state["sources"] = sorted({doc["source"] for doc in docs})
    return state
