from pdf_reader.application.config import build_runtime_config


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
                "profile": "ods_agenda_municipal_example",
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
    assert config.doc_type_generation.profile == "ods_agenda_municipal_example"
    assert config.doc_type_generation.output_path == "generated_doc_type.json"


def test_build_runtime_config_falls_back_to_generic_examples():
    config = build_runtime_config({})

    assert config.processing.output_file == "result.xml"
    assert config.processing.doc_type_path == "doc_type.json"
    assert config.comparison.output_file == "differences.json"
    assert len(config.comparison.targets) == 3
    assert config.doc_type_generation.profile == "generic_example"
