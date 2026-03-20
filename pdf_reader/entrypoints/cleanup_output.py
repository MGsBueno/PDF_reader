import os

from pdf_reader.application.cleanup_output import cleanup_output_dir
from pdf_reader.application.config import load_runtime_config
from pdf_reader.entrypoints._cli import parse_config_path


def main():
    # Exemplo de execucao:
    # python -m pdf_reader.entrypoints.cleanup_output --config .\config.json
    config = load_runtime_config(parse_config_path())
    if not config:
        return

    cleanup_output_dir(config.output_dir)


if __name__ == "__main__":
    main()
