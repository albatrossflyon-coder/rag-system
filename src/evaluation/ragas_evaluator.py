"""Evaluate RAG quality using Ragas metrics (not vibes)."""

from typing import Any, Dict, List

try:
    from datasets import Dataset
    from ragas import evaluate
    from ragas.metrics import answer_relevancy, context_precision, faithfulness
    _RAGAS_AVAILABLE = True
except ImportError:
    _RAGAS_AVAILABLE = False


class RagasEvaluator:
    """Evaluate RAG output with ground-truth Q&A pairs."""

    def __init__(self, faithfulness_threshold: float = 0.75, relevance_threshold: float = 0.80):
        self.faithfulness_threshold = faithfulness_threshold
        self.relevance_threshold = relevance_threshold

    def evaluate_batch(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Evaluate a batch of RAG results.
        Each result must have: question, answer, contexts (list of strings).
        Optional: ground_truth string for comparison.
        """
        if not _RAGAS_AVAILABLE:
            raise RuntimeError(
                "ragas and datasets packages are required for evaluation. "
                "Install them with: pip install ragas datasets"
            )

        eval_data = {
            "question": [r["question"] for r in results],
            "answer": [r["answer"] for r in results],
            "contexts": [r["contexts"] for r in results],
        }

        dataset = Dataset.from_dict(eval_data)
        eval_results = evaluate(
            dataset,
            metrics=[faithfulness, answer_relevancy, context_precision],
        )

        scores = eval_results.to_pandas()
        faith = float(scores["faithfulness"].mean())
        relevancy = float(scores["answer_relevancy"].mean())
        precision = float(scores["context_precision"].mean())

        return {
            "faithfulness": faith,
            "answer_relevancy": relevancy,
            "context_precision": precision,
            "passed": faith >= self.faithfulness_threshold and relevancy >= self.relevance_threshold,
        }
