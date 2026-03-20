import json
import os
from dataclasses import dataclass, field
from typing import Any, cast


@dataclass(frozen=True)
class ProcessingConfig:
    output_file: str = "result.xml"
    doc_type_path: str = "doc_type.json"


@dataclass(frozen=True)
class ComparisonTarget:
    name: str
    path: str


@dataclass(frozen=True)
class ComparisonConfig:
    targets: list[ComparisonTarget] = field(default_factory=list)
    output_file: str = "differences.json"


@dataclass(frozen=True)
class DocTypeGenerationConfig:
    profile: str = "generic_example"
    output_path: str = "doc_type.json"


@dataclass(frozen=True)
class RuntimeConfig:
    input_dir: str = "./input"
    output_dir: str = "./output"
    processing: ProcessingConfig = field(default_factory=ProcessingConfig)
    comparison: ComparisonConfig = field(default_factory=ComparisonConfig)
    doc_type_generation: DocTypeGenerationConfig = field(
        default_factory=DocTypeGenerationConfig
    )


def _load_dotenv(env_path: str) -> dict[str, str]:
    if not os.path.exists(env_path):
        return {}

    loaded_values: dict[str, str] = {}
    with open(env_path, "r", encoding="utf-8") as file:
        for raw_line in file:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip("'").strip('"')
            loaded_values[key] = value
            os.environ.setdefault(key, value)

    return loaded_values


def _expand_env_value(value: Any) -> Any:
    if isinstance(value, str):
        return os.path.expandvars(value)
    if isinstance(value, list):
        return [_expand_env_value(item) for item in value]
    if isinstance(value, dict):
        return {key: _expand_env_value(item) for key, item in value.items()}
    return value


def _env_or_value(env_name: str, current_value: str) -> str:
    return os.getenv(env_name, current_value)


def _apply_env_overrides(data: dict[str, Any]) -> dict[str, Any]:
    runtime_data = cast(dict[str, Any], _expand_env_value(data))
    processing_data = dict(runtime_data.get("processing", {}))
    comparison_data = dict(runtime_data.get("comparison", {}))
    doc_type_generation_data = dict(runtime_data.get("doc_type_generation", {}))

    runtime_data["input_dir"] = _env_or_value(
        "PDF_BATCH_EXTRACTOR_INPUT_DIR", runtime_data.get("input_dir", "./input")
    )
    runtime_data["output_dir"] = _env_or_value(
        "PDF_BATCH_EXTRACTOR_OUTPUT_DIR", runtime_data.get("output_dir", "./output")
    )

    processing_data["output_file"] = _env_or_value(
        "PDF_BATCH_EXTRACTOR_OUTPUT_FILE",
        processing_data.get("output_file", "result.xml"),
    )
    processing_data["doc_type_path"] = _env_or_value(
        "PDF_BATCH_EXTRACTOR_DOC_TYPE_PATH",
        processing_data.get("doc_type_path", "doc_type.json"),
    )

    comparison_data["output_file"] = _env_or_value(
        "PDF_BATCH_EXTRACTOR_COMPARISON_OUTPUT_FILE",
        comparison_data.get("output_file", "differences.json"),
    )

    doc_type_generation_data["profile"] = _env_or_value(
        "PDF_BATCH_EXTRACTOR_DOC_TYPE_PROFILE",
        doc_type_generation_data.get("profile", "generic_example"),
    )
    doc_type_generation_data["output_path"] = _env_or_value(
        "PDF_BATCH_EXTRACTOR_DOC_TYPE_OUTPUT_PATH",
        doc_type_generation_data.get("output_path", "doc_type.json"),
    )

    runtime_data["processing"] = processing_data
    runtime_data["comparison"] = comparison_data
    runtime_data["doc_type_generation"] = doc_type_generation_data
    return runtime_data


def _resolve_path(base_dir: str, path: str) -> str:
    if os.path.isabs(path):
        return path
    return os.path.abspath(os.path.join(base_dir, path))


def _build_comparison_targets(
    raw_targets: list[dict[str, Any]] | None,
) -> list[ComparisonTarget]:
    if not raw_targets:
        return [
            ComparisonTarget(name="extractor_a", path="./output/extractor_a"),
            ComparisonTarget(name="extractor_b", path="./output/extractor_b"),
            ComparisonTarget(name="extractor_c", path="./output/extractor_c"),
        ]

    return [
        ComparisonTarget(name=target["name"], path=target["path"])
        for target in raw_targets
    ]


def build_runtime_config(data: dict[str, Any]) -> RuntimeConfig:
    processing_data = data.get("processing", {})
    comparison_data = data.get("comparison", {})
    doc_type_generation_data = data.get("doc_type_generation", {})

    return RuntimeConfig(
        input_dir=data.get("input_dir", "./input"),
        output_dir=data.get("output_dir", "./output"),
        processing=ProcessingConfig(
            output_file=processing_data.get("output_file", "result.xml"),
            doc_type_path=processing_data.get("doc_type_path", "doc_type.json"),
        ),
        comparison=ComparisonConfig(
            targets=_build_comparison_targets(comparison_data.get("targets")),
            output_file=comparison_data.get("output_file", "differences.json"),
        ),
        doc_type_generation=DocTypeGenerationConfig(
            profile=doc_type_generation_data.get("profile", "generic_example"),
            output_path=doc_type_generation_data.get("output_path", "doc_type.json"),
        ),
    )


def load_runtime_config(config_path: str = "config.json") -> RuntimeConfig | None:
    if not os.path.exists(config_path):
        print(f"Configuration file {config_path} was not found.")
        return None

    base_dir = os.path.dirname(os.path.abspath(config_path))
    _load_dotenv(os.path.join(base_dir, ".env"))

    with open(config_path, "r", encoding="utf-8") as file:
        raw_data = json.load(file)

    if not isinstance(raw_data, dict):
        raise ValueError("Configuration file must contain a JSON object")

    config = build_runtime_config(_apply_env_overrides(cast(dict[str, Any], raw_data)))

    return RuntimeConfig(
        input_dir=_resolve_path(base_dir, config.input_dir),
        output_dir=_resolve_path(base_dir, config.output_dir),
        processing=ProcessingConfig(
            output_file=config.processing.output_file,
            doc_type_path=_resolve_path(base_dir, config.processing.doc_type_path),
        ),
        comparison=ComparisonConfig(
            targets=[
                ComparisonTarget(
                    name=target.name, path=_resolve_path(base_dir, target.path)
                )
                for target in config.comparison.targets
            ],
            output_file=config.comparison.output_file,
        ),
        doc_type_generation=DocTypeGenerationConfig(
            profile=config.doc_type_generation.profile,
            output_path=_resolve_path(base_dir, config.doc_type_generation.output_path),
        ),
    )
