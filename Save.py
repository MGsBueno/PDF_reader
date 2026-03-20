import os
import json
import time
from MyPdfMuPDF import MyPdfMuPDF

def carregar_config():
    config_path = "config.json"
    
    if not os.path.exists(config_path):
        print(f"O arquivo de configuração {config_path} não foi encontrado.")
        return None
    
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    return config


def processar_pdf_com_metodo(metodo, metodo_nome):
    start_time = time.time()
    metodo.processar()
    end_time = time.time()
    tempo_execucao = end_time - start_time
    
    print(f"Processamento concluído com {metodo_nome}.")
    print(f"Tempo de execução de {metodo_nome}: {tempo_execucao:.2f} segundos.")


def main():
    config = carregar_config()
    if not config:
        return

    origem_dir = os.path.abspath(config.get("input_dir", "pdfs"))
    destino_dir = os.path.abspath(config.get("output_dir", "output"))

    if not os.path.exists(origem_dir):
        print(f"A pasta {origem_dir} não existe. Verifique o caminho.")
        return

    if not os.path.exists(destino_dir):
        os.makedirs(destino_dir, exist_ok=True)

    arquivos_pdf = [os.path.join(origem_dir, f) for f in os.listdir(origem_dir) if f.lower().endswith(".pdf")]

    if not arquivos_pdf:
        print(f"Nenhum arquivo PDF encontrado na pasta {origem_dir}.")
        return

    # Caminho único para o XML de saída
    arquivo_saida_xml = os.path.join(destino_dir, "dump.xml")

    # Caminho para o json doc_type
    doc_type_path = "doc_type.json"

    print(f"Processando {len(arquivos_pdf)} arquivos PDF...")

    metodo_mupdf = MyPdfMuPDF(arquivos_pdf, arquivo_saida_xml, doc_type_path)
    processar_pdf_com_metodo(metodo_mupdf, "MyPdfMuPDF")


if __name__ == "__main__":
    main()
