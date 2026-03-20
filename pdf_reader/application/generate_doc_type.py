import json


def create_block(
    name,
    match=None,
    end_on_match=None,
    minimum_font_size=None,
    minimum_description_font_size=None,
    starts_structure=None,
    uses_description=None,
):
    block = {}
    if match is not None:
        block["match"] = match
    if end_on_match is not None:
        block["fim_ao_encontrar"] = end_on_match
    if minimum_font_size is not None:
        block["fonte_minima"] = minimum_font_size
    if minimum_description_font_size is not None:
        block["descricao_fonte_minima"] = minimum_description_font_size
    if starts_structure is not None:
        block["inicia_estrutura"] = starts_structure
    if uses_description is not None:
        block["usa_descricao"] = uses_description
    return name, block


def create_doc_type(blocks, ignore=None, block_names=None):
    if ignore is None:
        ignore = []

    if block_names is None:
        block_names = []

    return {
        "estruturas": {
            "blocos": dict(blocks),
            "ignorar": ignore,
            "nomes_blocos": block_names,
        }
    }


def save_json(data, file_name="doc_type.json"):
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    print(f"Arquivo {file_name} criado com sucesso.")


def build_default_doc_type():
    block_names = [
        "Objetivo de Desenvolvimento Estratégico (ODS)",
        "Meta Global",
        "Meta Municipal",
        "Contextualização",
        "Indicadores",
        "Desafios Remanescentes",
        "Classificação de Governabilidade",
        "Resultados e Oportunidaddes",
        "Plano de Ação para Implementação da Agenda Municipal 20230",
        "AçõesEixos Temáticos",
        "Objetivos Estratégicos",
        "Metas",
        "Iniciativas",
        "Indicador",
        "Secretarias Responsáveis",
        "ODS Vinculado",
        "Informações Complementares",
        "Contexto",
        "Regionalização",
    ]

    blocks = []
    for name in block_names:
        pattern = [f"^{name.lower()}"]

        if name == "Objetivo de Desenvolvimento Estratégico (ODS)":
            pattern = [r"^(ods|objetivo de desenvolvimento estratégico\s*\(?ods\)?)"]
        elif name == "Meta Global":
            pattern = [r"^meta global"]
        elif name == "Meta Municipal":
            pattern = [r"^meta municipal"]
        elif name == "Contextualização":
            pattern = [r"^contextualização"]
        elif name == "Indicadores":
            pattern = [r"^indicadores", r"^indicadores priorizados"]
        elif name == "Desafios Remanescentes":
            pattern = [r"^desafios remanescentes"]
        elif name == "Classificação de Governabilidade":
            pattern = [r"^classificação de governabilidade"]
        elif name == "Resultados e Oportunidaddes":
            pattern = [r"^resultados e oportunidades"]
        elif name == "Plano de Ação para Implementação da Agenda Municipal 20230":
            pattern = [r"^plano de ação para implementação da agenda municipal 20230"]
        elif name == "AçõesEixos Temáticos":
            pattern = [r"^ações", r"^eixos temáticos"]
        elif name == "Objetivos Estratégicos":
            pattern = [r"^objetivos estratégicos?"]
        elif name == "Metas":
            pattern = [r"^metas$"]
        elif name == "Iniciativas":
            pattern = [r"^iniciativas"]
        elif name == "Indicador":
            pattern = [r"^indicador$"]
        elif name == "Secretarias Responsáveis":
            pattern = [r"^secretarias? responsáveis?"]
        elif name == "ODS Vinculado":
            pattern = [r"^ods vinculados?"]
        elif name == "Informações Complementares":
            pattern = [r"^informações complementares"]
        elif name == "Contexto":
            pattern = [r"^contexto"]
        elif name == "Regionalização":
            pattern = [r"^regionalização"]

        blocks.append(
            create_block(
                name,
                match=pattern,
                minimum_font_size=12,
                minimum_description_font_size=10,
            )
        )

    ignore = [
        "Página",
        "Agenda Municipal 2030",
        "Prefeitura de São Paulo",
        "Contextualização",
        "Desafios remanescentes",
    ]

    return create_doc_type(blocks, ignore, block_names)
