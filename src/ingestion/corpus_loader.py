"""Load corpus from various formats (markdown, PDF, JSON)."""

import json
from pathlib import Path
from typing import Any, Dict, List

class CorpusLoader:
    """Load documents from corpus directory."""
    
    def __init__(self, corpus_path: str = "data/corpus"):
        self.corpus_path = Path(corpus_path)
        
    def load_markdown(self) -> List[Dict[str, Any]]:
        """Load all .md files."""
        docs = []
        for md_file in self.corpus_path.glob("*.md"):
            docs.append({
                "content": md_file.read_text(encoding="utf-8"),
                "source": md_file.name,
                "format": "markdown"
            })
        return docs
    
    def load_json(self) -> List[Dict[str, Any]]:
        """Load all .json files (expects list of {text, metadata})."""
        docs = []
        for json_file in self.corpus_path.glob("*.json"):
            with open(json_file) as f:
                data = json.load(f)
                if isinstance(data, list):
                    for item in data:
                        docs.append({
                            "content": item.get("text", ""),
                            "source": json_file.name,
                            "format": "json",
                            "metadata": item.get("metadata", {})
                        })
        return docs
    
    def load_all(self) -> List[Dict[str, Any]]:
        """Load all supported formats."""
        all_docs = []
        all_docs.extend(self.load_markdown())
        all_docs.extend(self.load_json())
        return all_docs
