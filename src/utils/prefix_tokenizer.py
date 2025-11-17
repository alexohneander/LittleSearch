from __future__ import annotations

import re
from typing import List

from interfaces.tokenizer_interface import TokenizerInterface
from models.index_token import IndexToken


class PrefixTokenizer(TokenizerInterface):
    """Prefix tokenizer that generates prefixes for each word.

    Ported from the provided PHP implementation:
    - Normalizes text like `WordTokenizer` (lowercase, remove non-alphanum, collapse spaces)
    - Extracts words, then for each word generates prefixes from `min_prefix_length`
      up to the full word length
    - Returns unique prefixes as `IndexToken` instances with given weight
    """

    def __init__(self, min_prefix_length: int = 4, weight: int = 5) -> None:
        self.min_prefix_length = int(min_prefix_length)
        self.weight = int(weight)

    def _extract_words(self, text: str) -> List[str]:
        s = (text or "").strip().lower()
        s = re.sub(r'[^a-z0-9]', ' ', s)
        s = re.sub(r'\s+', ' ', s)
        words = [w for w in s.split(' ') if len(w) >= 2]
        return words

    def tokenize(self, text: str) -> List[IndexToken]:
        words = self._extract_words(text)

        prefixes = {}
        for word in words:
            word_len = len(word)
            for i in range(self.min_prefix_length, word_len + 1):
                prefix = word[:i]
                prefixes[prefix] = True

        # Preserve insertion order by iterating keys (Python 3.7+ dict preserves order)
        return [IndexToken(name=prefix, weight=self.weight) for prefix in prefixes.keys()]

    def get_weight(self) -> int:
        return self.weight
