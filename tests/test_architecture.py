from pdf_reader.application.process_pdf_batch import PdfBatchProcessor
from pdf_reader.domain.models import LineData


class FakeExtractor:
    def extract_lines(self, pdf_path: str) -> list[LineData]:
        return [
            LineData(text="Titulo Principal", font_size=12, is_bold=True),
            LineData(text="linha complementar", font_size=9, is_bold=False),
            LineData(text="fim", font_size=9, is_bold=False),
        ]


def test_pdf_batch_processor_uses_layers(tmp_path):
    doc_type_path = tmp_path / "doc_type.json"
    doc_type_path.write_text(
        """
{
  "estruturas": {
    "blocos": {
      "Titulo": {
        "match": ["^titulo"],
        "descricao_fonte_minima": 10
      }
    },
    "ignorar": ["fim"]
  }
}
        """.strip(),
        encoding="utf-8",
    )

    output_path = tmp_path / "saida.xml"
    processor = PdfBatchProcessor(line_extractor=FakeExtractor())
    processor.process(["fake.pdf"], str(output_path), str(doc_type_path))

    content = output_path.read_text(encoding="utf-8")
    assert "<dados>" in content
    assert "<Titulo>Titulo Principal linha complementar</Titulo>" in content
    assert "</dados>" in content
