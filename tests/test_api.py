import json
from api import criar_bloco, criar_doc_type, salvar_json

def test_criar_bloco_fields():
    nome, bloco = criar_bloco("Titulo", match=[r"^titulo"], fonte_minima=12)
    assert nome == "Titulo"
    assert bloco["match"] == [r"^titulo"]
    assert bloco["fonte_minima"] == 12


def test_criar_doc_type_structure(tmp_path):
    blocos = [("A", {"match": [r"^a"]})]
    doc_type = criar_doc_type(blocos, ignorar=["fim"], nomes_blocos=["A"])
    assert "estruturas" in doc_type
    assert doc_type["estruturas"]["blocos"]["A"]["match"] == [r"^a"]
    assert doc_type["estruturas"]["ignorar"] == ["fim"]


def test_salvar_json_writes_file(tmp_path):
    data = {"estruturas": {"blocos": {}}}
    path = tmp_path / "doc_type_test.json"
    salvar_json(data, nome_arquivo=str(path))
    with open(path, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    assert loaded == data
