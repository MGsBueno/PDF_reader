from pdf_batch_extractor.application.cleanup_output import cleanup_output_dir
from pdf_batch_extractor.application.config import load_runtime_config
from pdf_batch_extractor.entrypoints._cli import parse_config_path


def main():
    # Example execution:
    # python -m pdf_batch_extractor.entrypoints.cleanup_output --config .\config.json
    config = load_runtime_config(parse_config_path())
    if not config:
        return

    cleanup_output_dir(config.output_dir)


if __name__ == "__main__":
    main()

