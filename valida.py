import os
import json

# Função para carregar um JSON de um arquivo
def carregar_json(caminho):
    with open(caminho, 'r', encoding='utf-8') as f:
        return json.load(f)

# Função para comparar o conteúdo dos arquivos JSON
def comparar_jsons(json1, json2):
    # Comparar apenas os campos 'titulo' e 'texto' dentro de 'blocos'
    blocos1 = json1.get("blocos", [])
    blocos2 = json2.get("blocos", [])

    # Verificar se a quantidade de blocos é a mesma
    if len(blocos1) != len(blocos2):
        return False

    # Comparar cada bloco (titulo e texto)
    for bloco1, bloco2 in zip(blocos1, blocos2):
        if bloco1.get("titulo") != bloco2.get("titulo") or bloco1.get("texto") != bloco2.get("texto"):
            return False

    return True

# Função principal para comparar os arquivos JSON nas 3 pastas
def comparar_pastas(pasta1, pasta2, pasta3):
    arquivos_diferentes = []
    pastas_com_diferenca = {}

    # Listar todos os arquivos nas pastas
    arquivos_pasta1 = set(os.listdir(pasta1))
    arquivos_pasta2 = set(os.listdir(pasta2))
    arquivos_pasta3 = set(os.listdir(pasta3))

    # Encontrar arquivos que existem nas 3 pastas
    arquivos_comum = arquivos_pasta1.intersection(arquivos_pasta2, arquivos_pasta3)

    for arquivo in arquivos_comum:
        # Montar os caminhos completos dos arquivos
        caminho1 = os.path.join(pasta1, arquivo)
        caminho2 = os.path.join(pasta2, arquivo)
        caminho3 = os.path.join(pasta3, arquivo)

        try:
            # Carregar os JSONs
            json1 = carregar_json(caminho1)
            json2 = carregar_json(caminho2)
            json3 = carregar_json(caminho3)

            # Verificar se o conteúdo dos blocos 'titulo' e 'texto' é igual
            if not (comparar_jsons(json1, json2) and comparar_jsons(json2, json3) and comparar_jsons(json1, json3)):              
                # Verificar em qual pasta há diferença
                diferenca = []
                if not comparar_jsons(json1, json2):
                    diferenca.append("pasta1 vs pasta2")
                if not comparar_jsons(json2, json3):
                    diferenca.append("pasta2 vs pasta3")
                if not comparar_jsons(json1, json3):
                    diferenca.append("pasta1 vs pasta3")
                
                pastas_com_diferenca[arquivo] = diferenca

        except Exception as e:
            print(f"Erro ao comparar o arquivo {arquivo}: {e}")

    # Gerar a saída em formato JSON
    resultado = {
        "pastas_com_diferenca": pastas_com_diferenca
    }
    
    with open("output/diferencas.json", "w", encoding="utf-8") as saida:
        json.dump(resultado, saida, indent=4, sort_keys=True)

# Definir os caminhos das pastas
path = "./output/"
pasta1 = f"{path}myPdfMiner"
pasta2 = f"{path}myPdfMuPDF"
pasta3 = f"{path}myPdfPlumber"

# Chamar a função para comparar as pastas
comparar_pastas(pasta1, pasta2, pasta3)
print("comparação concluída!")
