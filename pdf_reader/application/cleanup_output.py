import os
import shutil


def cleanup_output_dir(output_path):
    if not os.path.exists(output_path):
        print(f"Directory '{output_path}' does not exist.")
        return

    for root, dirs, files in os.walk(output_path, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            try:
                os.remove(file_path)
                print(f"Removed file: {file_path}")
            except Exception as error:
                print(f"Error removing file {file_path}: {error}")

        for name in dirs:
            dir_path = os.path.join(root, name)
            try:
                shutil.rmtree(dir_path)
                print(f"Removed directory: {dir_path}")
            except Exception as error:
                print(f"Error removing directory {dir_path}: {error}")
