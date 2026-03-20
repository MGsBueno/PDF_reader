from pdf_batch_extractor.application.config import load_runtime_config
from pdf_batch_extractor.application.generate_doc_type import build_doc_type, save_json
from pdf_batch_extractor.entrypoints._cli import parse_config_path


def main():
    # Example execution:
    # python -m pdf_batch_extractor.entrypoints.generate_doc_type --config .\config.json
    config = load_runtime_config(parse_config_path())
    if not config:
        return

    doc_type = build_doc_type(config.doc_type_generation.profile)
    save_json(doc_type, file_name=config.doc_type_generation.output_path)


if __name__ == "__main__":
    main()

