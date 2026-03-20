from pdf_reader.domain.models import BlockContent
from pdf_reader.domain.services import serialize_block


class XmlBlockWriter:
    def __init__(self, output_path: str):
        self.output_path = output_path

    def start_document(self) -> None:
        with open(self.output_path, "w", encoding="utf-8") as file:
            file.write("<dados>\n")

    def write_block(self, block: BlockContent) -> None:
        with open(self.output_path, "a", encoding="utf-8") as file:
            file.write(f"{serialize_block(block)}\n")

    def finish_document(self) -> None:
        with open(self.output_path, "a", encoding="utf-8") as file:
            file.write("</dados>\n")
