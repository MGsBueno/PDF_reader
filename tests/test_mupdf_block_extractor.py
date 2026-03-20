import json

from pdf_reader.infrastructure.extractors.mupdf_block_extractor import MuPdfBlockExtractor


def test_detect_block(tmp_path):
    doc_type_path = tmp_path / "doc_type.json"
    doc_type = {
        "structures": {
            "blocks": {
                "Title": {
                    "match": [r"^title"],
                    "minimum_description_font_size": 10,
                }
            },
            "ignore": ["end"],
        }
    }
    with open(doc_type_path, "w", encoding="utf-8") as file:
        json.dump(doc_type, file, ensure_ascii=False)

    output_xml_path = tmp_path / "output.xml"
    parser = MuPdfBlockExtractor([], str(output_xml_path), str(doc_type_path))
    assert parser.detect_block("Title of Document", 11) == "Title"
    assert parser.detect_block("No block", 11) is None


def test_write_xml_entry(tmp_path):
    doc_type_path = tmp_path / "doc_type.json"
    with open(doc_type_path, "w", encoding="utf-8") as file:
        json.dump({"structures": {"blocks": {}, "ignore": []}}, file, ensure_ascii=False)

    output_xml_path = tmp_path / "output.xml"
    parser = MuPdfBlockExtractor([], str(output_xml_path), str(doc_type_path))
    parser.save_xml_entry("My Block (1)", "Text <a> & test")
    with open(output_xml_path, "r", encoding="utf-8") as file:
        content = file.read()
    assert "<My_Block_1>Text &lt;a&gt; &amp; test</My_Block_1>" in content
