import json

def criar_bloco(nome, match=None, fim_ao_encontrar=None,
                fonte_minima=None, descricao_fonte_minima=None,
                inicia_estrutura=None, usa_descricao=None):
    bloco = {}
    if match is not None:
        bloco["match"] = match
    if fim_ao_encontrar is not None:
        bloco["fim_ao_encontrar"] = fim_ao_encontrar
    if fonte_minima is not None:
        bloco["fonte_minima"] = fonte_minima
    if descricao_fonte_minima is not None:
        bloco["descricao_fonte_minima"] = descricao_fonte_minima
    if inicia_estrutura is not None:
        bloco["inicia_estrutura"] = inicia_estrutura
    if usa_descricao is not None:
        bloco["usa_descricao"] = usa_descricao
    return nome, bloco

def criar_doc_type(blocos, ignorar=None):
    if ignorar is None:
        ignorar = []
    return {
        "ODS": {
            "blocos": dict(blocos),
            "ignorar": ignorar
        }
    }

def salvar_json(data, nome_arquivo='doc_type.json'):
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Arquivo {nome_arquivo} criado com sucesso.")

# Preenchendo seus dados como exemplo
if __name__ == "__main__":
    blocos = []
    blocos.append(criar_bloco(
        "ODS",
        match=["^ods\\s*\\d+(\\.\\d+)?"],
        fonte_minima=10,
        descricao_fonte_minima=12,
        inicia_estrutura=True,
        usa_descricao=True
    ))
    blocos.append(criar_bloco(
        "Meta Global",
        match=["^meta global"],
        fim_ao_encontrar=["meta municipal"]
    ))
    blocos.append(criar_bloco(
        "Meta Municipal",
        match=["^meta municipal"],
        fim_ao_encontrar=["contextualizando"]
    ))
    blocos.append(criar_bloco(
        "Indicadores",
        match=["^indicadores", "^indicadores priorizados"],
        fim_ao_encontrar=[
            "desafios remanescentes",
            "governabilidade",
            "meta municipal",
            "^meta global"
        ]
    ))

    ignorar = [
        "Página",
        "Agenda Municipal 2030",
        "Prefeitura de São Paulo",
        "Contextualização",
        "Desafios remanescentes"
    ]

    doc_type = criar_doc_type(blocos, ignorar)
    salvar_json(doc_type)
