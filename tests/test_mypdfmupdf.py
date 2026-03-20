import json
from MyPdfMuPDF import MyPdfMuPDF

def test_criar_bloque_e_detectar_bloco(tmp_path):
    doc_type_path = tmp_path / "doc_type.json"
    doc_type = {
        "estruturas": {
            "blocos": {
                "Titulo": {
                    "match": [r"^titulo"],
                    "descricao_fonte_minima": 10
                }
            },
            "ignorar": ["fim"]
        }
    }
    with open(doc_type_path, "w", encoding="utf-8") as f:
        json.dump(doc_type, f, ensure_ascii=False)

    output_xml_path = tmp_path / "output.xml"
    parser = MyPdfMuPDF([], str(output_xml_path), str(doc_type_path))
    assert parser.detectar_bloco("Titulo do Documento", 11) == "Titulo"
    assert parser.detectar_bloco("Sem bloco", 11) is None


def test_salvar_entrada_xml_escapa_e_grava(tmp_path):
    doc_type_path = tmp_path / "doc_type.json"
    with open(doc_type_path, "w", encoding="utf-8") as f:
        json.dump({"estruturas": {"blocos": {}, "ignorar": []}}, f, ensure_ascii=False)

    output_xml_path = tmp_path / "output.xml"
    parser = MyPdfMuPDF([], str(output_xml_path), str(doc_type_path))
    parser.salvar_entrada_xml("Meu Bloco (1)", "Texto <a> & teste")
    with open(output_xml_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "<Meu_Bloco_1>Texto &lt;a&gt; &amp; teste</Meu_Bloco_1>" in content
