from pdf_reader.application.config import build_runtime_config, load_runtime_config
from pdf_reader.infrastructure.config_loader import JsonDocumentTypeConfigLoader


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


def test_load_runtime_config_uses_dotenv_overrides(tmp_path, monkeypatch):
    config_path = tmp_path / "config.json"
    config_path.write_text(
        """
{
  "input_dir": "./docs",
  "output_dir": "./artifacts",
  "processing": {
    "output_file": "config.xml",
    "doc_type_path": "./doc_type.json"
  },
  "doc_type_generation": {
    "profile": "generic_example",
    "output_path": "./generated/doc_type.json"
  }
}
        """.strip(),
        encoding="utf-8",
    )
    (tmp_path / ".env").write_text(
        """
PDF_READER_INPUT_DIR=./env-input
PDF_READER_OUTPUT_DIR=./env-output
PDF_READER_OUTPUT_FILE=env-result.xml
PDF_READER_DOC_TYPE_PATH=./schemas/env-doc-type.json
PDF_READER_DOC_TYPE_PROFILE=structured_report_example
PDF_READER_DOC_TYPE_OUTPUT_PATH=./generated/env-doc-type.json
        """.strip(),
        encoding="utf-8",
    )

    for key in (
        "PDF_READER_INPUT_DIR",
        "PDF_READER_OUTPUT_DIR",
        "PDF_READER_OUTPUT_FILE",
        "PDF_READER_DOC_TYPE_PATH",
        "PDF_READER_DOC_TYPE_PROFILE",
        "PDF_READER_DOC_TYPE_OUTPUT_PATH",
    ):
        monkeypatch.delenv(key, raising=False)

    config = load_runtime_config(str(config_path))

    assert config is not None
    assert config.input_dir == str((tmp_path / "env-input").resolve())
    assert config.output_dir == str((tmp_path / "env-output").resolve())
    assert config.processing.output_file == "env-result.xml"
    assert config.processing.doc_type_path == str((tmp_path / "schemas" / "env-doc-type.json").resolve())
    assert config.doc_type_generation.profile == "structured_report_example"
    assert config.doc_type_generation.output_path == str((tmp_path / "generated" / "env-doc-type.json").resolve())


def test_load_runtime_config_expands_env_placeholders(tmp_path, monkeypatch):
    monkeypatch.setenv("TEST_INPUT_DIR", "./placeholder-input")
    monkeypatch.setenv("TEST_OUTPUT_DIR", "./placeholder-output")

    config_path = tmp_path / "config.json"
    config_path.write_text(
        """
{
  "input_dir": "${TEST_INPUT_DIR}",
  "output_dir": "${TEST_OUTPUT_DIR}"
}
        """.strip(),
        encoding="utf-8",
    )

    config = load_runtime_config(str(config_path))

    assert config is not None
    assert config.input_dir == str((tmp_path / "placeholder-input").resolve())
    assert config.output_dir == str((tmp_path / "placeholder-output").resolve())


def test_document_type_config_loader_requires_structures_root(tmp_path):
    path = tmp_path / "doc_type.json"
    path.write_text('{"blocks": {}}', encoding="utf-8")

    loader = JsonDocumentTypeConfigLoader()

    try:
        loader.load(str(path))
        assert False, "Expected ValueError for missing 'structures' root"
    except ValueError as error:
        assert "top-level 'structures'" in str(error)


def test_document_type_config_loader_rejects_portuguese_keys(tmp_path):
    path = tmp_path / "doc_type.json"
    path.write_text(
        """
{
  "structures": {
    "blocos": {},
    "ignorar": []
  }
}
        """.strip(),
        encoding="utf-8",
    )

    loader = JsonDocumentTypeConfigLoader()

    try:
        loader.load(str(path))
        assert False, "Expected ValueError for Portuguese keys"
    except ValueError as error:
        assert "no longer supported" in str(error)
