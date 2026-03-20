from pdf_reader.application.process_pdf_batch import PdfBatchProcessor
from pdf_reader.domain.models import BlockContent, LineData
from pdf_reader.domain.services import BlockDetector, serialize_block
from pdf_reader.infrastructure.config_loader import JsonDocumentTypeConfigLoader


class MuPdfBlockExtractor:
    def __init__(self, pdf_paths, output_xml_path, doc_type_path):
        self.pdf_paths = pdf_paths
        self.output_xml_path = output_xml_path
        self.doc_type_path = doc_type_path
        self._config = None
        self._detector = None
        self._processor = PdfBatchProcessor()
        self.blocos_config = {}
        self.ignorar_textos = set()
        self.ordem_blocos = []
        self.load_config()

    def load_config(self):
        self._config = JsonDocumentTypeConfigLoader().load(self.doc_type_path)
        self._detector = BlockDetector(self._config)
        self.blocos_config = {
            block_name: {
                "match": rule.match,
                "descricao_fonte_minima": rule.descricao_fonte_minima,
            }
            for block_name, rule in self._config.blocos.items()
        }
        self.ignorar_textos = set(self._config.ignorar)
        self.ordem_blocos = list(self.blocos_config.keys())

    def detectar_bloco(self, texto, fonte):
        return self._detector.detect(LineData(text=texto, font_size=fonte, is_bold=True))

    def salvar_entrada_xml(self, nome_bloco, texto):
        with open(self.output_xml_path, "a", encoding="utf-8") as file:
            file.write(f"{serialize_block(BlockContent(name=nome_bloco, text=texto))}\n")

    def processar(self):
        self._processor.process(self.pdf_paths, self.output_xml_path, self.doc_type_path)
        print(f"XML final salvo em: {self.output_xml_path}")
