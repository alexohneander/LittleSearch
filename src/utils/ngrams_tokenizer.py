from __future__ import annotations

import re
from typing import List

from interfaces.tokenizer_interface import TokenizerInterface
from models.index_token import IndexToken


class NGramsTokenizer(TokenizerInterface):
    """N-gram tokenizer.

    Behavior ported from the provided PHP implementation:
    - Normalizes text like `WordTokenizer`/`PrefixTokenizer` (lowercase, remove non-alphanum, collapse spaces)
    - Extracts words, then for each word generates fixed-length n-grams using a sliding window
    - Returns unique n-grams as `IndexToken` instances with the given weight
    """

    def __init__(self, ngram_length: int = 3, weight: int = 1) -> None:
        self.ngram_length = int(ngram_length)
        self.weight = int(weight)

    def _extract_words(self, text: str) -> List[str]:
        s = (text or "").strip().lower()
        s = re.sub(r"[^a-z0-9]", " ", s)
        s = re.sub(r"\s+", " ", s)
        words = [w for w in s.split(" ") if len(w) >= 2]
        return words

    def tokenize(self, text: str) -> List[IndexToken]:
        words = self._extract_words(text)

        tokens = {}
        for word in words:
            word_len = len(word)
            # Sliding window of fixed length
            for i in range(0, word_len - self.ngram_length + 1):
                ngram = word[i : i + self.ngram_length]
                tokens[ngram] = True

        return [IndexToken(name=ngram, weight=self.weight) for ngram in tokens.keys()]

    def get_weight(self) -> int:
        return self.weight
