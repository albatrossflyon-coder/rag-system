"""Generate answers with Claude, enforcing citation."""

from typing import List, Tuple, Dict, Any
from langchain_openai import ChatAnthropic
from langchain.prompts import PromptTemplate

class ClaudeGenerator:
    """Generate grounded answers with inline citations."""
    
    def __init__(self, model: str = "claude-3-5-sonnet-20241022"):
        self.llm = ChatAnthropic(model_name=model)
        self.system_prompt = """You are a helpful assistant answering questions based on provided context.

IMPORTANT RULES:
1. Answer ONLY from the provided context.
2. If the context doesn't contain relevant information, say "I don't have information on this in the provided context."
3. Cite your sources inline using [Source: filename] format.
4. Be concise and accurate.
5. Do not make up information."""
    
    def generate(self, query: str, context: List[Tuple[str, float]]) -> Dict[str, Any]:
        """Generate answer from query + reranked context."""
        
        # Format context
        context_text = "\n\n".join([
            f"[Source: Unknown]\n{doc[0]}"
            for doc in context
        ])
        
        prompt = f"""Context:
{context_text}

Question: {query}

Answer:"""
        
        response = self.llm.invoke(self.system_prompt + "\n\n" + prompt)
        
        return {
            "answer": response.content,
            "sources": [doc[0][:100] for doc in context],  # First 100 chars as source snippet
            "confidence": "high"  # TODO: implement confidence scoring
        }
