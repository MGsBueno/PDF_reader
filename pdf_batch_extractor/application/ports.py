from collections.abc import Callable, Iterable
from typing import Protocol

from pdf_batch_extractor.domain.models import BlockContent, DocumentTypeConfig, LineData


class LineExtractor(Protocol):
    def extract_lines(self, pdf_path: str) -> list[LineData]: ...


class DocumentTypeConfigLoader(Protocol):
    def load(self, doc_type_path: str) -> DocumentTypeConfig: ...


class BlockWriter(Protocol):
    def start_document(self) -> None: ...

    def write_block(self, block: BlockContent) -> None: ...

    def finish_document(self) -> None: ...


BlockWriterFactory = Callable[[str], BlockWriter]
PdfPathCollection = Iterable[str]

