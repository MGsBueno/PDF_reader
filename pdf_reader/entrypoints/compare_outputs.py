import os

from pdf_reader.application.compare_outputs import compare_folders
from pdf_reader.application.config import ComparisonTarget, load_runtime_config


def main():
    config = load_runtime_config("config.json")
    if not config:
        return

    targets = [
        ComparisonTarget(name=target.name, path=os.path.abspath(target.path))
        for target in config.comparison.targets
    ]
    output_path = os.path.join(os.path.abspath(config.output_dir), config.comparison.output_file)
    compare_folders(targets, output_path)
    print("comparacao concluida!")


if __name__ == "__main__":
    main()
