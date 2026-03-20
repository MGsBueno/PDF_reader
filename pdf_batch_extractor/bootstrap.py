from pdf_batch_extractor.application.process_pdf_batch import PdfBatchProcessor
from pdf_batch_extractor.infrastructure.config_loader import (
    JsonDocumentTypeConfigLoader,
)
from pdf_batch_extractor.infrastructure.extractors.pymupdf_extractor import (
    PyMuPdfLineExtractor,
)
from pdf_batch_extractor.infrastructure.writers.xml_writer import XmlBlockWriter


def create_pdf_batch_processor() -> PdfBatchProcessor:
    return PdfBatchProcessor(
        line_extractor=PyMuPdfLineExtractor(),
        config_loader=JsonDocumentTypeConfigLoader(),
        writer_factory=XmlBlockWriter,
    )
