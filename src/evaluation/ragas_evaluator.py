"""Evaluate RAG quality using Ragas metrics (not vibes)."""

from typing import List, Dict, Any
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision
)
from datasets import Dataset

class RagasEvaluator:
    """Evaluate RAG output with ground-truth Q&A pairs."""
    
    def __init__(self, faithfulness_threshold: float = 0.75, relevance_threshold: float = 0.80):
        self.faithfulness_threshold = faithfulness_threshold
        self.relevance_threshold = relevance_threshold
    
    def evaluate_batch(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Evaluate batch of RAG results.
        Expected format:
        {
            "question": str,
            "answer": str,
            "contexts": List[str],
            "ground_truth": str  (optional, for comparison)
        }
        """
        
        # Convert to Ragas dataset format
        eval_data = {
            "question": [r["question"] for r in results],
            "answer": [r["answer"] for r in results],
            "contexts": [r["contexts"] for r in results],
        }
        
        dataset = Dataset.from_dict(eval_data)
        
        # Run evaluation
        eval_results = evaluate(
            dataset,
            metrics=[faithfulness, answer_relevancy, context_precision]
        )
        
        return {
            "faithfulness": float(eval_results["faithfulness"].mean()),
            "answer_relevancy": float(eval_results["answer_relevancy"].mean()),
            "context_precision": float(eval_results["context_precision"].mean()),
            "passed": (
                eval_results["faithfulness"].mean() >= self.faithfulness_threshold and
                eval_results["answer_relevancy"].mean() >= self.relevance_threshold
            )
        }
