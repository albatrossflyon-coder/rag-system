import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from config.settings import settings
from src.ingestion import CorpusLoader, SemanticChunker
from src.pipeline import bootstrap_corpus, new_pipeline_state
from src.retrieval import HybridRetriever


class BootstrapTests(unittest.TestCase):
    def test_settings_use_repo_relative_paths(self):
        self.assertEqual(settings.corpus_path, REPO_ROOT / "data" / "corpus")
        self.assertTrue(settings.corpus_path.exists())

    def test_bootstrap_populates_pipeline_state(self):
        loader = CorpusLoader(corpus_path=settings.corpus_path)
        chunker = SemanticChunker(chunk_size=512, overlap=50)
        retriever = HybridRetriever(top_k=3, use_pinecone=False)
        pipeline_state = new_pipeline_state()

        bootstrap_corpus(loader, chunker, retriever, settings.corpus_path, pipeline_state)

        self.assertTrue(pipeline_state["ready"])
        self.assertEqual(pipeline_state["documents"], 2)
        self.assertGreater(pipeline_state["chunks"], 2)
        self.assertEqual(pipeline_state["sources"], ["mcp-protocol.md", "superintendent-mcp.md"])


if __name__ == "__main__":
    unittest.main()
