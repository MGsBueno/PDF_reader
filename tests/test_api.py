import json
from pdf_reader.application.generate_doc_type import build_doc_type, create_block, create_doc_type, save_json

def test_create_block_fields():
    name, block = create_block("Title", match=[r"^title"], minimum_font_size=12)
    assert name == "Title"
    assert block["match"] == [r"^title"]
    assert block["minimum_font_size"] == 12


def test_create_doc_type_structure(tmp_path):
    blocks = [("A", {"match": [r"^a"]})]
    doc_type = create_doc_type(blocks, ignore=["end"], block_names=["A"])
    assert "structures" in doc_type
    assert doc_type["structures"]["blocks"]["A"]["match"] == [r"^a"]
    assert doc_type["structures"]["ignore"] == ["end"]


def test_save_json_writes_file(tmp_path):
    data = {"structures": {"blocks": {}}}
    path = tmp_path / "doc_type_test.json"
    save_json(data, file_name=str(path))
    with open(path, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    assert loaded == data


def test_build_doc_type_uses_generic_profile_by_name():
    doc_type = build_doc_type("generic_example")
    assert "structures" in doc_type
    assert "Title" in doc_type["structures"]["blocks"]
    assert doc_type["structures"]["ignore"] == ["Page", "Header", "Footer"]
