import os

from pdf_reader.application.cleanup_output import cleanup_output_dir
from pdf_reader.application.config import load_runtime_config


def main():
    config = load_runtime_config("config.json")
    if not config:
        return

    cleanup_output_dir(os.path.abspath(config.output_dir))


if __name__ == "__main__":
    main()
