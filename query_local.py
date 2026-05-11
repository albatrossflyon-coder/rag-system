#!/usr/bin/env python3
"""Query the local corpus without running the FastAPI server."""

import argparse

from config.settings import settings
from src.generation import ClaudeGenerator
from src.ingestion import CorpusLoader, SemanticChunker
from src.pipeline import bootstrap_corpus, new_pipeline_state
from src.reranking import CrossEncoderReranker
from src.retrieval import HybridRetriever


def build_pipeline():
    loader = CorpusLoader(corpus_path=settings.corpus_path)
    chunker = SemanticChunker(chunk_size=settings.chunk_max_tokens, overlap=settings.chunk_overlap)
    retriever = HybridRetriever(top_k=settings.retrieval_top_k, use_pinecone=settings.deployment_env == "production")
    reranker = CrossEncoderReranker(use_cohere=bool(settings.cohere_api_key))
    pipeline_state = new_pipeline_state()
    bootstrap_corpus(loader, chunker, retriever, settings.corpus_path, pipeline_state)
    return retriever, reranker, pipeline_state


def main() -> None:
    parser = argparse.ArgumentParser(description="Query the local RAG corpus.")
    parser.add_argument("query", help="Question to run against the local corpus")
    parser.add_argument("--top-k", type=int, default=settings.rerank_top_k, help="How many reranked chunks to keep")
    parser.add_argument("--answer", action="store_true", help="Generate a final answer with Anthropic if ANTHROPIC_API_KEY is set")
    args = parser.parse_args()

    retriever, reranker, pipeline_state = build_pipeline()
    results = retriever.retrieve_hybrid(args.query)
    reranked = reranker.rerank(args.query, results, top_k=args.top_k)

    print(f"Corpus ready: {pipeline_state['documents']} documents, {pipeline_state['chunks']} chunks")
    print(f"Query: {args.query}\n")

    for index, document in enumerate(reranked, start=1):
        snippet = document["content"][:180].replace("\n", " ")
        print(f"{index}. {document['source']} | rerank={document.get('rerank_score', 0):.3f} | fusion={document.get('fusion_score', 0):.3f}")
        print(f"   {snippet}")

    if not args.answer:
        return

    generator = ClaudeGenerator()
    response = generator.generate(args.query, reranked)
    print("\nAnswer:\n")
    print(response["answer"])
    print(f"\nSources: {', '.join(response['sources'])}")


if __name__ == "__main__":
    main()
