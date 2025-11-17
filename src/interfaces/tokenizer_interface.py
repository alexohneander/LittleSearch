from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from models.index_token import IndexToken


class TokenizerInterface(ABC):
    """Abstract tokenizer interface.
    Implementations should return a list of `IndexToken` objects from `tokenize`
    and an integer weight from `get_weight`.
    """

    @abstractmethod
    def tokenize(self, text: str) -> List[IndexToken]:
        """Tokenize the given text and return a list of `IndexToken` objects.

        Args:
            text: The input string to tokenize.

        Returns:
            A list of `IndexToken` instances representing tokens extracted from the text.
        """
        raise NotImplementedError

    @abstractmethod
    def get_weight(self) -> int:
        """Return the tokenizer's weight as an integer.

        Higher weight tokenizers may be preferred when combining multiple tokenizers.
        """
        raise NotImplementedError
