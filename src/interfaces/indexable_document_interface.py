from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


DocumentType = Any
IndexableFields = Any


class IndexableDocumentInterface(ABC):
	"""Interface for documents that can be indexed.

	Methods mirror the PHP interface:
	- get_document_id() -> int
	- get_document_type() -> DocumentType
	- get_indexable_fields() -> IndexableFields
	"""

	@abstractmethod
	def get_document_id(self) -> int:
		"""Return the unique integer id for the document."""
		raise NotImplementedError

	@abstractmethod
	def get_document_type(self) -> 'DocumentType':
		"""Return the document's type.

		The concrete `DocumentType` class or enum should be defined elsewhere
		in the project. A forward reference is used here to avoid import
		cycles.
		"""
		raise NotImplementedError

	@abstractmethod
	def get_indexable_fields(self) -> 'IndexableFields':
		"""Return the indexable fields for the document.

		The `IndexableFields` type should be defined elsewhere in the codebase.
		"""
		raise NotImplementedError

