import json

from pdf_reader.domain.models import BlockRule, DocumentTypeConfig


class JsonDocumentTypeConfigLoader:
    def load(self, doc_type_path: str) -> DocumentTypeConfig:
        with open(doc_type_path, "r", encoding="utf-8") as file:
            doc_type = json.load(file)

        for category in doc_type.values():
            if not isinstance(category, dict):
                continue

            blocks_key = "blocks" if "blocks" in category else "blocos" if "blocos" in category else None
            ignore_key = "ignore" if "ignore" in category else "ignorar" if "ignorar" in category else None

            if blocks_key and ignore_key:
                rules = {
                    block_name: BlockRule(
                        match=block_config.get("match", []),
                        minimum_description_font_size=block_config.get(
                            "minimum_description_font_size",
                            block_config.get("descricao_fonte_minima", 0),
                        ),
                    )
                    for block_name, block_config in category.get(blocks_key, {}).items()
                }
                return DocumentTypeConfig(
                    blocks=rules,
                    ignore=set(category.get(ignore_key, [])),
                )

        return DocumentTypeConfig()
