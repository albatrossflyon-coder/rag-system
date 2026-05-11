"""Generate grounded answers with Claude via the Anthropic Messages API."""

import os
import json
from typing import Any, Dict, List
from urllib import error, request

from config.settings import settings


class ClaudeGenerator:
    """Generate grounded answers with inline citations."""

    def __init__(self, model: str = "claude-sonnet-4-6", max_tokens: int = 700):
        self.model = model
        self.max_tokens = max_tokens
        self.api_key = settings.anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
        self.system_prompt = """You are a helpful assistant answering questions based on provided context.

IMPORTANT RULES:
1. Answer ONLY from the provided context.
2. If the context doesn't contain relevant information, say "I don't have information on this in the provided context."
3. Cite your sources inline using [Source: filename] format.
4. Be concise and accurate.
5. Do not make up information."""

    def generate(self, query: str, context: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate an answer from a reranked context list."""
        if not context:
            raise ValueError("No retrieved context is available to answer from.")
        if not self.api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is required to generate answers.")

        context_text = "\n\n".join(
            f"[Source: {document.get('source', 'unknown')}]\n{document['content']}"
            for document in context
        )

        payload = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": 0,
            "system": self.system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": (
                        f"Context:\n{context_text}\n\n"
                        f"Question: {query}\n\n"
                        "Answer:"
                    ),
                }
            ],
        }

        http_request = request.Request(
            "https://api.anthropic.com/v1/messages",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            method="POST",
        )
        try:
            with request.urlopen(http_request, timeout=60) as response:
                body = json.loads(response.read().decode("utf-8"))
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Anthropic API request failed: {detail}") from exc

        answer = "".join(
            item.get("text", "")
            for item in body.get("content", [])
            if item.get("type") == "text"
        ).strip()

        return {
            "answer": answer,
            "sources": sorted({document.get("source", "unknown") for document in context}),
            "confidence": "high" if len(context) >= 2 else "medium",
        }
