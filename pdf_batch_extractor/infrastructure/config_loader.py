import json

from pdf_batch_extractor.domain.models import BlockRule, DocumentTypeConfig


class JsonDocumentTypeConfigLoader:
    def load(self, doc_type_path: str) -> DocumentTypeConfig:
        with open(doc_type_path, "r", encoding="utf-8") as file:
            doc_type = json.load(file)

        if not isinstance(doc_type, dict):
            raise ValueError("Document type configuration must be a JSON object.")

        if "structures" not in doc_type:
            raise ValueError(
                "Document type configuration must contain a top-level 'structures' object."
            )

        structures = doc_type["structures"]
        if not isinstance(structures, dict):
            raise ValueError("'structures' must be a JSON object.")

        if "blocos" in structures or "ignorar" in structures:
            raise ValueError(
                "Portuguese document type keys are no longer supported. Use 'blocks' and 'ignore'."
            )

        if "blocks" not in structures or "ignore" not in structures:
            raise ValueError("'structures' must define both 'blocks' and 'ignore'.")

        blocks = structures["blocks"]
        ignore = structures["ignore"]

        if not isinstance(blocks, dict):
            raise ValueError("'blocks' must be a JSON object keyed by block name.")
        if not isinstance(ignore, list):
            raise ValueError("'ignore' must be a JSON array of prefixes.")

        rules = {
            block_name: self._build_block_rule(block_name, block_config)
            for block_name, block_config in blocks.items()
        }
        return DocumentTypeConfig(blocks=rules, ignore=set(ignore))

    def _build_block_rule(self, block_name: str, block_config: dict) -> BlockRule:
        if not isinstance(block_config, dict):
            raise ValueError(f"Block '{block_name}' must be a JSON object.")

        match = block_config.get("match")
        if not isinstance(match, list) or not all(
            isinstance(pattern, str) for pattern in match
        ):
            raise ValueError(
                f"Block '{block_name}' must define 'match' as a list of regex strings."
            )

        minimum_description_font_size = block_config.get(
            "minimum_description_font_size", 0
        )
        if not isinstance(minimum_description_font_size, (int, float)):
            raise ValueError(
                f"Block '{block_name}' must define 'minimum_description_font_size' as a number when present."
            )

        return BlockRule(
            match=match,
            minimum_description_font_size=float(minimum_description_font_size),
        )
