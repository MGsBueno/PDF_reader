import fitz

from pdf_reader.domain.models import LineData


class PyMuPdfLineExtractor:
    def extract_lines(self, pdf_path: str) -> list[LineData]:
        lines: list[LineData] = []

        with fitz.open(pdf_path) as document:
            for page in document:
                blocks = page.get_text("dict")["blocks"]
                for block in blocks:
                    if "lines" not in block:
                        continue

                    for line in block["lines"]:
                        spans = line["spans"]
                        if not spans:
                            continue

                        text = " ".join(span["text"] for span in spans).strip()
                        if not text:
                            continue

                        lines.append(
                            LineData(
                                text=text,
                                font_size=max(span["size"] for span in spans),
                                is_bold=any(
                                    "bold" in span.get("font", "").lower()
                                    for span in spans
                                ),
                            )
                        )

        return lines
