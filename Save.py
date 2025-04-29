import os
import json
import time
from MyPdfMuPDF import MyPdfMuPDF

def carregar_config():
    """
    Carrega as configurações de caminho de origem e saída a partir do arquivo config.json.
    """
    config_path = "config.json"
    
    if not os.path.exists(config_path):
        print(f"O arquivo de configuração {config_path} não foi encontrado.")
        return None
    
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    return config


def processar_pdf_com_metodo(pdf_path, pdf_output_dir, metodo, metodo_nome):
    """
    Processa o PDF usando o método especificado e salva os resultados em JSON por página.
    """
    start_time = time.time()
    
    metodo.extrair_texto()
    
    end_time = time.time()
    tempo_execucao = end_time - start_time
    
    print(f"Processamento concluído com {metodo_nome}.")
    print(f"Tempo de execução de {metodo_nome}: {tempo_execucao:.2f} segundos.")


def main():
    """
    Função principal que lida com os argumentos e chama a função de processamento.
    """
    config = carregar_config()
    
    if not config:
        return
    
    origem_dir = os.path.abspath(config.get("input_dir"))
    destino_dir = os.path.abspath(config.get("output_dir"))
    
    if not os.path.exists(origem_dir):
        print(f"A pasta {origem_dir} não existe. Verifique o caminho.")
        return
    
    os.makedirs(destino_dir, exist_ok=True)
    
    arquivos_pdf = [f for f in os.listdir(origem_dir) if f.lower().endswith(".pdf")]
    
    if not arquivos_pdf:
        print(f"Nenhum arquivo PDF encontrado na pasta {origem_dir}.")
        return
    
    for pdf_file in arquivos_pdf:
        pdf_path = os.path.join(origem_dir, pdf_file)
        print(f"Processando o PDF: {pdf_file}")
        
        pdf_output_dir = os.path.join(destino_dir, os.path.splitext(pdf_file)[0])
        os.makedirs(pdf_output_dir, exist_ok=True)
     
        metodo_mupdf = MyPdfMuPDF(pdf_path, pdf_output_dir, "config.json","doc_type.json")
        processar_pdf_com_metodo(pdf_path, pdf_output_dir, metodo_mupdf, "myPdfMuPDF")


if __name__ == "__main__":
    main()
