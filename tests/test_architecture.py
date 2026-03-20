from pdf_batch_extractor.application.process_pdf_batch import PdfBatchProcessor
from pdf_batch_extractor.domain.models import LineData


class FakeExtractor:
    def extract_lines(self, pdf_path: str) -> list[LineData]:
        return [
            LineData(text="Title Main", font_size=12, is_bold=True),
            LineData(text="complementary line", font_size=9, is_bold=False),
            LineData(text="end", font_size=9, is_bold=False),
        ]


class FakeConfigLoader:
    def load(self, doc_type_path: str):
        from pdf_batch_extractor.domain.models import BlockRule, DocumentTypeConfig

        return DocumentTypeConfig(
            blocks={
                "Title": BlockRule(match=[r"^title"], minimum_description_font_size=10)
            },
            ignore={"end"},
        )


class FakeWriter:
    def __init__(self, output_path: str):
        self.output_path = output_path

    def start_document(self) -> None:
        with open(self.output_path, "w", encoding="utf-8") as file:
            file.write("<data>\n")

    def write_block(self, block) -> None:
        with open(self.output_path, "a", encoding="utf-8") as file:
            file.write(f"  <{block.name}>{block.text}</{block.name}>\n")

    def finish_document(self) -> None:
        with open(self.output_path, "a", encoding="utf-8") as file:
            file.write("</data>\n")


def test_pdf_batch_processor_uses_layers(tmp_path):
    output_path = tmp_path / "output.xml"
    processor = PdfBatchProcessor(
        line_extractor=FakeExtractor(),
        config_loader=FakeConfigLoader(),
        writer_factory=FakeWriter,
    )
    processor.process(["fake.pdf"], str(output_path), "unused.json")

    content = output_path.read_text(encoding="utf-8")
    assert "<data>" in content
    assert "<Title>Title Main complementary line</Title>" in content
    assert "</data>" in content
