import json
import os
from dataclasses import dataclass, field


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
    doc_type_generation: DocTypeGenerationConfig = field(default_factory=DocTypeGenerationConfig)


def _resolve_path(base_dir: str, path: str) -> str:
    if os.path.isabs(path):
        return path
    return os.path.abspath(os.path.join(base_dir, path))


def _build_comparison_targets(raw_targets: list[dict] | None) -> list[ComparisonTarget]:
    if not raw_targets:
        # Example local execution targets. Override them in config.json to compare your own contexts.
        return [
            ComparisonTarget(name="extractor_a", path="./output/extractor_a"),
            ComparisonTarget(name="extractor_b", path="./output/extractor_b"),
            ComparisonTarget(name="extractor_c", path="./output/extractor_c"),
        ]

    return [ComparisonTarget(name=target["name"], path=target["path"]) for target in raw_targets]


def build_runtime_config(data: dict) -> RuntimeConfig:
    processing_data = data.get("processing", {})
    comparison_data = data.get("comparison", {})
    doc_type_generation_data = data.get("doc_type_generation", {})

    return RuntimeConfig(
        input_dir=data.get("input_dir", "./input"),
        output_dir=data.get("output_dir", "./output"),
        processing=ProcessingConfig(
            # Example execution default. Override it in config.json for custom pipelines.
            output_file=processing_data.get("output_file", "result.xml"),
            # Example execution default. Override it in config.json for other schemas.
            doc_type_path=processing_data.get("doc_type_path", "doc_type.json"),
        ),
        comparison=ComparisonConfig(
            targets=_build_comparison_targets(comparison_data.get("targets")),
            # Example execution default. Override it in config.json for custom reports.
            output_file=comparison_data.get("output_file", "differences.json"),
        ),
        doc_type_generation=DocTypeGenerationConfig(
            # Example profile. Use any supported profile name or add your own profile definition.
            profile=doc_type_generation_data.get("profile", "generic_example"),
            output_path=doc_type_generation_data.get("output_path", "doc_type.json"),
        ),
    )


def load_runtime_config(config_path: str = "config.json") -> RuntimeConfig | None:
    if not os.path.exists(config_path):
        print(f"O arquivo de configuracao {config_path} nao foi encontrado.")
        return None

    with open(config_path, "r", encoding="utf-8") as file:
        config = build_runtime_config(json.load(file))

    base_dir = os.path.dirname(os.path.abspath(config_path))
    return RuntimeConfig(
        input_dir=_resolve_path(base_dir, config.input_dir),
        output_dir=_resolve_path(base_dir, config.output_dir),
        processing=ProcessingConfig(
            output_file=config.processing.output_file,
            doc_type_path=_resolve_path(base_dir, config.processing.doc_type_path),
        ),
        comparison=ComparisonConfig(
            targets=[
                ComparisonTarget(name=target.name, path=_resolve_path(base_dir, target.path))
                for target in config.comparison.targets
            ],
            output_file=config.comparison.output_file,
        ),
        doc_type_generation=DocTypeGenerationConfig(
            profile=config.doc_type_generation.profile,
            output_path=_resolve_path(base_dir, config.doc_type_generation.output_path),
        ),
    )
