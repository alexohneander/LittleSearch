from __future__ import annotations

import math
from typing import Dict, Iterable, List, Optional

from interfaces.indexable_document_interface import IndexableDocumentInterface
from interfaces.tokenizer_interface import TokenizerInterface
from models.index_entry import IndexEntry
from models.index_token import IndexToken
from sqlmodel import Session, select
from sqlalchemy import delete as sa_delete


class SearchIndexingService:
    """Python port of the provided PHP SearchIndexingService.

    Responsibilities:
    - Remove any existing index entries for a document
    - Run configured tokenizers over each indexable field
    - Ensure tokens exist in `index_tokens` (find-or-create)
    - Batch-insert `index_entries` with computed weights
    """

    def __init__(self, session: Session, tokenizers: Iterable[TokenizerInterface]):
        self.session = session
        self.tokenizers = list(tokenizers)

    def index_document(self, document: IndexableDocumentInterface) -> None:
        # 1. Get document info
        document_type = document.get_document_type()
        # If document_type is an enum-like object, use its value
        document_type_value = getattr(document_type, "value", document_type)
        document_id = document.get_document_id()

        indexable_fields = document.get_indexable_fields()

        # attempt to retrieve fields and weights using common patterns
        fields: Dict = {}
        weights: Dict = {}
        if hasattr(indexable_fields, "get_fields"):
            fields = indexable_fields.get_fields() or {}
        elif hasattr(indexable_fields, "fields"):
            fields = getattr(indexable_fields, "fields") or {}
        elif isinstance(indexable_fields, dict):
            fields = indexable_fields.get("fields", indexable_fields) or {}

        if hasattr(indexable_fields, "get_weights"):
            weights = indexable_fields.get_weights() or {}
        elif hasattr(indexable_fields, "weights"):
            weights = getattr(indexable_fields, "weights") or {}
        elif isinstance(indexable_fields, dict):
            weights = indexable_fields.get("weights", {}) or {}

        # 2. Remove existing index for this document
        self._remove_document_index(document_type_value, document_id)

        # 3. Prepare batch insert data
        insert_entries: List[IndexEntry] = []

        # 4. Process each field
        for field_id_value, content in (fields or {}).items():
            if not content:
                continue

            # normalize field id (support enum-like values)
            field_id = getattr(field_id_value, "value", field_id_value)
            field_weight = int(
                weights.get(field_id_value, 0) or weights.get(field_id, 0) or 0
            )

            # 5. Run all tokenizers on this field
            for tokenizer in self.tokenizers:
                tokens = tokenizer.tokenize(content)
                for token in tokens:
                    # tokenizer IndexToken uses `name` and `weight`
                    token_value = getattr(token, "name", None)
                    token_weight = int(
                        getattr(token, "weight", tokenizer.get_weight() or 0) or 0
                    )

                    if not token_value:
                        continue

                    # 6. Find or create token in index_tokens
                    token_id = self.find_or_create_token(token_value, token_weight)

                    # 7. Calculate final weight
                    token_length = len(token_value)
                    final_weight = int(
                        field_weight
                        * token_weight
                        * math.ceil(math.sqrt(max(1, token_length)))
                    )

                    # 8. Add to batch insert (create IndexEntry object)
                    entry = IndexEntry(
                        token_id=int(token_id),
                        document_type=int(document_type_value),
                        field_id=int(field_id),
                        document_id=int(document_id),
                        weight=int(final_weight),
                    )
                    insert_entries.append(entry)

        # 9. Batch insert for performance
        if insert_entries:
            self._batch_insert_search_documents(insert_entries)

    def find_or_create_token(self, name: str, weight: int) -> int:
        """Find existing token by name+weight or create it and return its id."""
        stmt = select(IndexToken).where(
            IndexToken.name == name, IndexToken.weight == weight
        )
        result = self.session.exec(stmt).first()
        if result:
            return int(result.id)

        token = IndexToken(name=name, weight=int(weight))
        self.session.add(token)
        self.session.commit()
        self.session.refresh(token)
        return int(token.id)

    def _remove_document_index(self, document_type: int, document_id: int) -> None:
        # Efficient delete using SQLAlchemy core delete
        delete_stmt = sa_delete(IndexEntry).where(
            IndexEntry.document_type == int(document_type),
            IndexEntry.document_id == int(document_id),
        )
        self.session.exec(delete_stmt)
        self.session.commit()

    def _batch_insert_search_documents(self, entries: List[IndexEntry]) -> None:
        # Use bulk save for performance
        self.session.add_all(entries)
        self.session.commit()
