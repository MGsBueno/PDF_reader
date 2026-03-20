import re
from xml.sax.saxutils import escape

from pdf_reader.domain.models import BlockContent, DocumentTypeConfig, LineData


class BlockDetector:
    def __init__(self, config: DocumentTypeConfig):
        self._config = config

    def detect(self, line: LineData) -> str | None:
        if not line.is_bold:
            return None

        text_lower = line.text.lower()
        for block_name, rule in self._config.blocos.items():
            for pattern in rule.match:
                if re.match(pattern, text_lower, re.IGNORECASE) and line.font_size >= rule.descricao_fonte_minima:
                    return block_name
        return None

    def should_ignore(self, text: str) -> bool:
        text_lower = text.lower()
        return any(text_lower.startswith(ignored.lower()) for ignored in self._config.ignorar)


def build_xml_tag(block_name: str) -> str:
    return block_name.replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_")


def serialize_block(block: BlockContent) -> str:
    tag = build_xml_tag(block.name)
    escaped_text = escape(block.text.strip())
    return f"  <{tag}>{escaped_text}</{tag}>"
