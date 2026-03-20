import os

from pdf_reader.application.compare_outputs import compare_folders
from pdf_reader.application.config import ComparisonTarget, load_runtime_config
from pdf_reader.entrypoints._cli import parse_config_path


def main():
    # Example execution:
    # python -m pdf_reader.entrypoints.compare_outputs --config .\config.json
    config = load_runtime_config(parse_config_path())
    if not config:
        return

    targets = [
        ComparisonTarget(name=target.name, path=target.path)
        for target in config.comparison.targets
    ]
    output_path = os.path.join(config.output_dir, config.comparison.output_file)
    compare_folders(targets, output_path)
    print("Comparison completed!")


if __name__ == "__main__":
    main()
