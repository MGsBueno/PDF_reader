from pdf_reader.application.process_pdf_batch import PdfBatchProcessor
from pdf_reader.domain.models import LineData


class FakeExtractor:
    def extract_lines(self, pdf_path: str) -> list[LineData]:
        return [
            LineData(text="Title Main", font_size=12, is_bold=True),
            LineData(text="complementary line", font_size=9, is_bold=False),
            LineData(text="end", font_size=9, is_bold=False),
        ]


def test_pdf_batch_processor_uses_layers(tmp_path):
    doc_type_path = tmp_path / "doc_type.json"
    doc_type_path.write_text(
        """
{
  "structures": {
    "blocks": {
      "Title": {
        "match": ["^title"],
        "minimum_description_font_size": 10
      }
    },
    "ignore": ["end"]
  }
}
        """.strip(),
        encoding="utf-8",
    )

    output_path = tmp_path / "output.xml"
    processor = PdfBatchProcessor(line_extractor=FakeExtractor())
    processor.process(["fake.pdf"], str(output_path), str(doc_type_path))

    content = output_path.read_text(encoding="utf-8")
    assert "<data>" in content
    assert "<Title>Title Main complementary line</Title>" in content
    assert "</data>" in content
