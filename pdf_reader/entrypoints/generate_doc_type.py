from pdf_reader.application.generate_doc_type import build_default_doc_type, save_json


def main():
    save_json(build_default_doc_type())


if __name__ == "__main__":
    main()
