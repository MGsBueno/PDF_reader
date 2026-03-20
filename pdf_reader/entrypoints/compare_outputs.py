import os

from pdf_reader.application.compare_outputs import compare_folders


def main():
    output_dir = "./output/"
    folder1 = os.path.join(output_dir, "myPdfMiner")
    folder2 = os.path.join(output_dir, "myPdfMuPDF")
    folder3 = os.path.join(output_dir, "myPdfPlumber")
    output_path = os.path.join(output_dir, "diferencas.json")
    compare_folders(folder1, folder2, folder3, output_path)
    print("comparacao concluida!")


if __name__ == "__main__":
    main()
