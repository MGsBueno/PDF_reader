from pdf_reader.application.process_pdf_batch import PdfBatchProcessor
from pdf_reader.infrastructure.config_loader import JsonDocumentTypeConfigLoader
from pdf_reader.infrastructure.extractors.pymupdf_extractor import PyMuPdfLineExtractor
from pdf_reader.infrastructure.writers.xml_writer import XmlBlockWriter


def create_pdf_batch_processor() -> PdfBatchProcessor:
    return PdfBatchProcessor(
        line_extractor=PyMuPdfLineExtractor(),
        config_loader=JsonDocumentTypeConfigLoader(),
        writer_factory=XmlBlockWriter,
    )
