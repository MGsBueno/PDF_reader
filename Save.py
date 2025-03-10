import os
import json
import time
from MyPdfPlumber import MyPdfPlumber
from MyPdfMuPDF import MyPdfMuPDF
from MyPdfMiner import MyPdfMiner

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
    
    :param pdf_path: Caminho do arquivo PDF a ser processado
    :param pdf_output_dir: Diretório específico do arquivo PDF
    :param metodo: Instância do método de extração a ser utilizado
    :param metodo_nome: Nome do método de extração para criar o diretório
    """
    start_time = time.time()  # Marca o início do tempo
    
    metodo.extrair_texto()
    
    # Cria um diretório separado para cada método de extração dentro da pasta do arquivo PDF
    metodo_output_dir = os.path.join(pdf_output_dir, metodo_nome)
    os.makedirs(metodo_output_dir, exist_ok=True)
    
    end_time = time.time()  # Marca o fim do tempo
    tempo_execucao = end_time - start_time  # Calcula o tempo de execução
    
    print(f"Processamento concluído com {metodo_nome}. Arquivos JSON salvos em {metodo_output_dir}.")
    print(f"Tempo de execução de {metodo_nome}: {tempo_execucao:.2f} segundos.")


def main():
    """
    Função principal que lida com os argumentos e chama a função de processamento.
    """
    config = carregar_config()
    
    if not config:
        return
    
    # Caminhos relativos definidos no arquivo config.json
    origem_dir = os.path.abspath(config.get("input_dir"))
    destino_dir = os.path.abspath(config.get("output_dir"))
    
    # Verifica se a pasta origem existe
    if not os.path.exists(origem_dir):
        print(f"A pasta {origem_dir} não existe. Verifique o caminho.")
        return
    
    # Cria o diretório de saída se não existir
    os.makedirs(destino_dir, exist_ok=True)
    
    # Lista todos os arquivos PDF na pasta origem
    arquivos_pdf = [f for f in os.listdir(origem_dir) if f.lower().endswith(".pdf")]
    
    if not arquivos_pdf:
        print(f"Nenhum arquivo PDF encontrado na pasta {origem_dir}.")
        return
    
    # Processa cada arquivo PDF na pasta origem com os três métodos
    for pdf_file in arquivos_pdf:
        pdf_path = os.path.join(origem_dir, pdf_file)
        print(f"Processando o PDF: {pdf_file}")
        
        # Criando diretório específico para o arquivo PDF
        pdf_output_dir = os.path.join(destino_dir, os.path.splitext(pdf_file)[0])
        os.makedirs(pdf_output_dir, exist_ok=True)
        
        # Usando MyPdfPlumber
        metodo_plumber = MyPdfPlumber(pdf_path, pdf_output_dir, "config.json")
        processar_pdf_com_metodo(pdf_path, pdf_output_dir, metodo_plumber, "myPdfPlumber")
        
        # Usando MyPdfMuPDF
        metodo_mupdf = MyPdfMuPDF(pdf_path, pdf_output_dir, "config.json")
        processar_pdf_com_metodo(pdf_path, pdf_output_dir, metodo_mupdf, "myPdfMuPDF")
        
        # Usando MyPdfMiner
        metodo_miner = MyPdfMiner(pdf_path, pdf_output_dir, "config.json")
        processar_pdf_com_metodo(pdf_path, pdf_output_dir, metodo_miner, "myPdfMiner")


if __name__ == "__main__":
    main()