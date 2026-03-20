from pdf_reader.application.config import build_runtime_config, load_runtime_config


def test_build_runtime_config_uses_explicit_values():
    config = build_runtime_config(
        {
            "input_dir": "./docs",
            "output_dir": "./artifacts",
            "processing": {
                "output_file": "custom.xml",
                "doc_type_path": "custom_doc_type.json",
            },
            "comparison": {
                "output_file": "report.json",
                "targets": [
                    {"name": "a", "path": "./artifacts/a"},
                    {"name": "b", "path": "./artifacts/b"},
                ],
            },
            "doc_type_generation": {
                "profile": "structured_report_example",
                "output_path": "generated_doc_type.json",
            },
        }
    )

    assert config.input_dir == "./docs"
    assert config.output_dir == "./artifacts"
    assert config.processing.output_file == "custom.xml"
    assert config.processing.doc_type_path == "custom_doc_type.json"
    assert [target.name for target in config.comparison.targets] == ["a", "b"]
    assert config.comparison.output_file == "report.json"
    assert config.doc_type_generation.profile == "structured_report_example"
    assert config.doc_type_generation.output_path == "generated_doc_type.json"


def test_build_runtime_config_falls_back_to_generic_examples():
    config = build_runtime_config({})

    assert config.processing.output_file == "result.xml"
    assert config.processing.doc_type_path == "doc_type.json"
    assert config.comparison.output_file == "differences.json"
    assert len(config.comparison.targets) == 3
    assert config.doc_type_generation.profile == "generic_example"


def test_load_runtime_config_resolves_paths_from_config_directory(tmp_path):
    config_path = tmp_path / "nested" / "config.json"
    config_path.parent.mkdir()
    config_path.write_text(
        """
{
  "input_dir": "./docs",
  "output_dir": "./artifacts",
  "processing": {
    "doc_type_path": "schemas/doc_type.json"
  },
  "comparison": {
    "targets": [
      { "name": "a", "path": "./artifacts/a" }
    ]
  },
  "doc_type_generation": {
    "output_path": "./generated/doc_type.json"
  }
}
        """.strip(),
        encoding="utf-8",
    )

    config = load_runtime_config(str(config_path))

    assert config is not None
    assert config.input_dir == str((config_path.parent / "docs").resolve())
    assert config.output_dir == str((config_path.parent / "artifacts").resolve())
    assert config.processing.doc_type_path == str((config_path.parent / "schemas" / "doc_type.json").resolve())
    assert config.comparison.targets[0].path == str((config_path.parent / "artifacts" / "a").resolve())
    assert config.doc_type_generation.output_path == str((config_path.parent / "generated" / "doc_type.json").resolve())
