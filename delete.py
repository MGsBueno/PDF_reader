import os
import shutil

def delete(caminho_output):
    # Verifica se o diretório 'output' existe
    if os.path.exists(caminho_output):
        # Percorre todas as pastas e arquivos dentro de 'output'
        for root, dirs, files in os.walk(caminho_output, topdown=False):
            for name in files:
                try:
                    file_path = os.path.join(root, name)
                    os.remove(file_path)
                    print(f"Arquivo removido: {file_path}")
                except Exception as e:
                    print(f"Erro ao remover o arquivo {file_path}: {e}")
            for name in dirs:
                try:
                    dir_path = os.path.join(root, name)
                    shutil.rmtree(dir_path)  # Remove subdiretórios
                    print(f"Pasta removida: {dir_path}")
                except Exception as e:
                    print(f"Erro ao remover a pasta {dir_path}: {e}")
    else:
        print(f"O diretório '{caminho_output}' não existe.")

if __name__ == "__main__":
    caminho_output = './output/'  # Caminho da pasta output
    delete(caminho_output)
