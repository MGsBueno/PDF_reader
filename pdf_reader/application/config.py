import json
import os


def load_runtime_config(config_path: str = "config.json") -> dict | None:
    if not os.path.exists(config_path):
        print(f"O arquivo de configuracao {config_path} nao foi encontrado.")
        return None

    with open(config_path, "r", encoding="utf-8") as file:
        return json.load(file)
