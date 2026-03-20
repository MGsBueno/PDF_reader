import json
import os


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def compare_jsons(json1, json2):
    blocks1 = json1.get("blocos", [])
    blocks2 = json2.get("blocos", [])

    if len(blocks1) != len(blocks2):
        return False

    for block1, block2 in zip(blocks1, blocks2):
        if block1.get("titulo") != block2.get("titulo") or block1.get("texto") != block2.get("texto"):
            return False

    return True


def compare_folders(folder1, folder2, folder3, output_path):
    differences = {}

    files1 = set(os.listdir(folder1))
    files2 = set(os.listdir(folder2))
    files3 = set(os.listdir(folder3))
    common_files = files1.intersection(files2, files3)

    for file_name in common_files:
        path1 = os.path.join(folder1, file_name)
        path2 = os.path.join(folder2, file_name)
        path3 = os.path.join(folder3, file_name)

        try:
            json1 = load_json(path1)
            json2 = load_json(path2)
            json3 = load_json(path3)

            if not (compare_jsons(json1, json2) and compare_jsons(json2, json3) and compare_jsons(json1, json3)):
                difference = []
                if not compare_jsons(json1, json2):
                    difference.append("pasta1 vs pasta2")
                if not compare_jsons(json2, json3):
                    difference.append("pasta2 vs pasta3")
                if not compare_jsons(json1, json3):
                    difference.append("pasta1 vs pasta3")
                differences[file_name] = difference
        except Exception as error:
            print(f"Erro ao comparar o arquivo {file_name}: {error}")

    result = {"pastas_com_diferenca": differences}
    with open(output_path, "w", encoding="utf-8") as output_file:
        json.dump(result, output_file, indent=4, sort_keys=True)

    return result
