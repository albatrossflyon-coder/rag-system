import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.ingestion import CorpusLoader, SemanticChunker
from src.retrieval import HybridRetriever
from src.reranking import CrossEncoderReranker


class Phase1BPipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        loader = CorpusLoader(corpus_path=REPO_ROOT / "data" / "corpus")
        cls.docs = loader.load_all()
        cls.chunker = SemanticChunker(chunk_size=512, overlap=50)
        cls.chunks = cls.chunker.chunk_documents(cls.docs)
        cls.retriever = HybridRetriever(top_k=3, use_pinecone=False)
        cls.retriever.index_documents(cls.chunks)

    def test_loads_markdown_corpus(self):
        sources = {doc["source"] for doc in self.docs}
        self.assertEqual(sources, {"mcp-protocol.md", "superintendent-mcp.md"})
        self.assertEqual(len(self.docs), 2)

    def test_chunks_preserve_source_metadata(self):
        self.assertGreater(len(self.chunks), 2)
        self.assertTrue(all("source" in chunk for chunk in self.chunks))
        self.assertTrue(all("chunk_index" in chunk for chunk in self.chunks))

    def test_hybrid_retrieval_finds_mcp_overview(self):
        results = self.retriever.retrieve_hybrid("What is MCP?")
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0]["source"], "mcp-protocol.md")

    def test_local_reranker_keeps_best_content_first(self):
        retriever_results = self.retriever.retrieve_hybrid("content scheduling API")
        reranker = CrossEncoderReranker(use_cohere=False)
        reranked = reranker.rerank("content scheduling API", retriever_results, top_k=2)
        self.assertGreater(len(reranked), 0)
        self.assertEqual(reranked[0]["source"], "superintendent-mcp.md")


if __name__ == "__main__":
    unittest.main()
