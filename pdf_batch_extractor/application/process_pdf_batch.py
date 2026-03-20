import os
import time

from pdf_batch_extractor.domain.models import BlockContent
from pdf_batch_extractor.domain.services import BlockDetector
from pdf_batch_extractor.application.ports import (
    BlockWriter,
    BlockWriterFactory,
    DocumentTypeConfigLoader,
    LineExtractor,
)


class PdfBatchProcessor:
    def __init__(
        self,
        line_extractor: LineExtractor,
        config_loader: DocumentTypeConfigLoader,
        writer_factory: BlockWriterFactory,
    ):
        self._line_extractor = line_extractor
        self._config_loader = config_loader
        self._writer_factory = writer_factory

    def process(
        self, pdf_paths: list[str], output_xml_path: str, doc_type_path: str
    ) -> None:
        config = self._config_loader.load(doc_type_path)
        detector = BlockDetector(config)
        writer = self._writer_factory(output_xml_path)

        writer.start_document()
        for pdf_path in pdf_paths:
            self._process_single_pdf(pdf_path, detector, writer)
        writer.finish_document()

    def _process_single_pdf(
        self, pdf_path: str, detector: BlockDetector, writer: BlockWriter
    ) -> None:
        current_block_name: str | None = None
        current_text = ""

        for line in self._line_extractor.extract_lines(pdf_path):
            if detector.should_ignore(line.text):
                if current_block_name:
                    writer.write_block(
                        BlockContent(name=current_block_name, text=current_text.strip())
                    )
                    current_block_name = None
                    current_text = ""
                continue

            block_name = detector.detect(line)
            if block_name:
                if current_block_name:
                    writer.write_block(
                        BlockContent(name=current_block_name, text=current_text.strip())
                    )
                current_block_name = block_name
                current_text = line.text
                continue

            if current_block_name:
                current_text += f" {line.text}"

        if current_block_name:
            writer.write_block(
                BlockContent(name=current_block_name, text=current_text.strip())
            )


def collect_pdf_paths(input_dir: str) -> list[str]:
    return [
        os.path.join(input_dir, file_name)
        for file_name in os.listdir(input_dir)
        if file_name.lower().endswith(".pdf")
    ]


def run_processing_job(
    processor: PdfBatchProcessor,
    pdf_paths: list[str],
    output_xml_path: str,
    doc_type_path: str,
    method_name: str,
) -> None:
    start_time = time.time()
    processor.process(pdf_paths, output_xml_path, doc_type_path)
    elapsed_time = time.time() - start_time
    print(f"Processing completed with {method_name}.")
    print(f"Execution time for {method_name}: {elapsed_time:.2f} seconds.")
