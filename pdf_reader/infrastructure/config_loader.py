import json

from pdf_reader.domain.models import BlockRule, DocumentTypeConfig


class JsonDocumentTypeConfigLoader:
    def load(self, doc_type_path: str) -> DocumentTypeConfig:
        with open(doc_type_path, "r", encoding="utf-8") as file:
            doc_type = json.load(file)

        for category in doc_type.values():
            if isinstance(category, dict) and "blocos" in category and "ignorar" in category:
                rules = {
                    block_name: BlockRule(
                        match=block_config.get("match", []),
                        descricao_fonte_minima=block_config.get("descricao_fonte_minima", 0),
                    )
                    for block_name, block_config in category.get("blocos", {}).items()
                }
                return DocumentTypeConfig(
                    blocos=rules,
                    ignorar=set(category.get("ignorar", [])),
                )

        return DocumentTypeConfig()
