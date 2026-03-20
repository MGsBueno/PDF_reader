import warnings

from pdf_reader.bootstrap import create_pdf_batch_processor
from pdf_reader.domain.models import BlockContent, LineData
from pdf_reader.domain.services import BlockDetector, serialize_block
from pdf_reader.infrastructure.config_loader import JsonDocumentTypeConfigLoader


class MuPdfBlockExtractor:
    """Legacy compatibility wrapper around the main PDF batch processor."""

    def __init__(self, pdf_paths, output_xml_path, doc_type_path):
        warnings.warn(
            "MuPdfBlockExtractor is a legacy compatibility wrapper. "
            "Prefer PdfBatchProcessor via the composition root for new integrations.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.pdf_paths = pdf_paths
        self.output_xml_path = output_xml_path
        self.doc_type_path = doc_type_path
        self._config = None
        self._detector = None
        self._processor = create_pdf_batch_processor()
        self.block_config = {}
        self.ignored_texts = set()
        self.block_order = []
        self.load_config()

    def load_config(self):
        self._config = JsonDocumentTypeConfigLoader().load(self.doc_type_path)
        self._detector = BlockDetector(self._config)
        self.block_config = {
            block_name: {
                "match": rule.match,
                "minimum_description_font_size": rule.minimum_description_font_size,
            }
            for block_name, rule in self._config.blocks.items()
        }
        self.ignored_texts = set(self._config.ignore)
        self.block_order = list(self.block_config.keys())

    def detect_block(self, text, font_size):
        return self._detector.detect(
            LineData(text=text, font_size=font_size, is_bold=True)
        )

    def save_xml_entry(self, block_name, text):
        with open(self.output_xml_path, "a", encoding="utf-8") as file:
            file.write(f"{serialize_block(BlockContent(name=block_name, text=text))}\n")

    def process(self):
        self._processor.process(
            self.pdf_paths, self.output_xml_path, self.doc_type_path
        )
        print(f"Final XML saved to: {self.output_xml_path}")

    def detectar_bloco(self, texto, fonte):
        return self.detect_block(texto, fonte)

    def salvar_entrada_xml(self, nome_bloco, texto):
        self.save_xml_entry(nome_bloco, texto)

    def processar(self):
        self.process()
