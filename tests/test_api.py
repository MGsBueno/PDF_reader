import json
from pdf_reader.application.generate_doc_type import create_block, create_doc_type, save_json

def test_criar_bloco_fields():
    nome, bloco = create_block("Titulo", match=[r"^titulo"], minimum_font_size=12)
    assert nome == "Titulo"
    assert bloco["match"] == [r"^titulo"]
    assert bloco["fonte_minima"] == 12


def test_criar_doc_type_structure(tmp_path):
    blocos = [("A", {"match": [r"^a"]})]
    doc_type = create_doc_type(blocos, ignore=["fim"], block_names=["A"])
    assert "estruturas" in doc_type
    assert doc_type["estruturas"]["blocos"]["A"]["match"] == [r"^a"]
    assert doc_type["estruturas"]["ignorar"] == ["fim"]


def test_salvar_json_writes_file(tmp_path):
    data = {"estruturas": {"blocos": {}}}
    path = tmp_path / "doc_type_test.json"
    save_json(data, file_name=str(path))
    with open(path, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    assert loaded == data
