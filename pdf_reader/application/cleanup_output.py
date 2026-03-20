import os
import shutil


def cleanup_output_dir(output_path):
    if not os.path.exists(output_path):
        print(f"O diretorio '{output_path}' nao existe.")
        return

    for root, dirs, files in os.walk(output_path, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            try:
                os.remove(file_path)
                print(f"Arquivo removido: {file_path}")
            except Exception as error:
                print(f"Erro ao remover o arquivo {file_path}: {error}")

        for name in dirs:
            dir_path = os.path.join(root, name)
            try:
                shutil.rmtree(dir_path)
                print(f"Pasta removida: {dir_path}")
            except Exception as error:
                print(f"Erro ao remover a pasta {dir_path}: {error}")
