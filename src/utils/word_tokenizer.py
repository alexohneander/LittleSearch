from __future__ import annotations

import re
from typing import List

from interfaces.tokenizer_interface import TokenizerInterface
from models.index_token import IndexToken


class WordTokenizer(TokenizerInterface):
    """Whitespace/word tokenizer.

    Behavior ported from the provided PHP code:
    - Lowercase and trim input
    - Replace non-alphanumeric characters with spaces
    - Collapse multiple whitespace into single spaces
    - Split into words, remove duplicates and short words (<2 chars)
    - Return a list of `IndexToken` objects with the tokenizer's weight
    """

    def __init__(self, weight: int = 1) -> None:
        self.weight = int(weight)

    def tokenize(self, text: str) -> List[IndexToken]:
        if not isinstance(text, str):
            text = str(text)

        # Normalize: lowercase, trim
        s = text.strip().lower()

        # Replace non a-z0-9 with space (mirrors PHP pattern)
        s = re.sub(r"[^a-z0-9]", " ", s)

        # Collapse multiple whitespace into single space
        s = re.sub(r"\s+", " ", s)

        # Split into words and filter short ones
        words = [w for w in s.split(" ") if len(w) >= 2]

        # Remove duplicates while preserving order
        seen = set()
        unique_words: List[str] = []
        for w in words:
            if w not in seen:
                seen.add(w)
                unique_words.append(w)

        # Map to IndexToken objects
        tokens: List[IndexToken] = [
            IndexToken(name=w, weight=self.weight) for w in unique_words
        ]
        return tokens

    def get_weight(self) -> int:
        return self.weight
