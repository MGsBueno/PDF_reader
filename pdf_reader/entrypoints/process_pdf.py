import os

from pdf_reader.application.config import load_runtime_config
from pdf_reader.application.process_pdf_batch import PdfBatchProcessor, collect_pdf_paths, run_processing_job
from pdf_reader.entrypoints._cli import parse_config_path


def main():
    # Exemplo de execucao:
    # python -m pdf_reader.entrypoints.process_pdf --config .\config.json
    config = load_runtime_config(parse_config_path())
    if not config:
        return

    input_dir = config.input_dir
    output_dir = config.output_dir

    if not os.path.exists(input_dir):
        print(f"A pasta {input_dir} nao existe. Verifique o caminho.")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    pdf_files = collect_pdf_paths(input_dir)
    if not pdf_files:
        print(f"Nenhum arquivo PDF encontrado na pasta {input_dir}.")
        return

    output_xml_path = os.path.join(output_dir, config.processing.output_file)
    doc_type_path = config.processing.doc_type_path

    print(f"Processando {len(pdf_files)} arquivos PDF...")
    processor = PdfBatchProcessor()
    run_processing_job(processor, pdf_files, output_xml_path, doc_type_path, "PyMuPDF")


if __name__ == "__main__":
    main()
