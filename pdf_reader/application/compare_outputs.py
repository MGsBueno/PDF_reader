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


def compare_folders(targets, output_path):
    differences = {}
    if len(targets) < 2:
        raise ValueError("At least two comparison targets are required.")

    files_by_target = {target.name: set(os.listdir(target.path)) for target in targets}
    common_files = set.intersection(*(files for files in files_by_target.values()))

    for file_name in common_files:
        try:
            loaded_jsons = {
                target.name: load_json(os.path.join(target.path, file_name))
                for target in targets
            }
            target_names = list(loaded_jsons.keys())
            difference = []

            for index, left_name in enumerate(target_names):
                for right_name in target_names[index + 1 :]:
                    if not compare_jsons(loaded_jsons[left_name], loaded_jsons[right_name]):
                        difference.append(f"{left_name} vs {right_name}")

            if difference:
                differences[file_name] = difference
        except Exception as error:
            print(f"Erro ao comparar o arquivo {file_name}: {error}")

    result = {"pastas_com_diferenca": differences}
    with open(output_path, "w", encoding="utf-8") as output_file:
        json.dump(result, output_file, indent=4, sort_keys=True)

    return result
