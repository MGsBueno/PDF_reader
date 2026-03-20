import argparse


def parse_config_path(default_path: str = "config.json") -> str:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--config", default=default_path)
    args, _ = parser.parse_known_args()

    if not isinstance(args.config, str):
        raise ValueError("config must be a string")

    return args.config
