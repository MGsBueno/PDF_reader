import json


PROFILE_LIBRARY = {
    "generic_example": {
        "context_name": "estruturas",
        "block_names": ["Titulo", "Subtitulo", "Resumo", "Detalhes"],
        "rules": {
            "Titulo": [r"^titulo"],
            "Subtitulo": [r"^subtitulo"],
            "Resumo": [r"^resumo"],
            "Detalhes": [r"^detalhes"],
        },
        "ignore": ["Pagina", "Cabecalho", "Rodape"],
        "minimum_font_size": 12,
        "minimum_description_font_size": 10,
    },
    "ods_agenda_municipal_example": {
        "context_name": "estruturas",
        "block_names": [
            "Objetivo de Desenvolvimento Estrategico (ODS)",
            "Meta Global",
            "Meta Municipal",
            "Contextualizacao",
            "Indicadores",
            "Desafios Remanescentes",
            "Classificacao de Governabilidade",
            "Resultados e Oportunidaddes",
            "Plano de Acao para Implementacao da Agenda Municipal 20230",
            "AcoesEixos Tematicos",
            "Objetivos Estrategicos",
            "Metas",
            "Iniciativas",
            "Indicador",
            "Secretarias Responsaveis",
            "ODS Vinculado",
            "Informacoes Complementares",
            "Contexto",
            "Regionalizacao",
        ],
        "rules": {
            "Objetivo de Desenvolvimento Estrategico (ODS)": [r"^(ods|objetivo de desenvolvimento estrategico\s*\(?ods\)?)"],
            "Meta Global": [r"^meta global"],
            "Meta Municipal": [r"^meta municipal"],
            "Contextualizacao": [r"^contextualizacao"],
            "Indicadores": [r"^indicadores", r"^indicadores priorizados"],
            "Desafios Remanescentes": [r"^desafios remanescentes"],
            "Classificacao de Governabilidade": [r"^classificacao de governabilidade"],
            "Resultados e Oportunidaddes": [r"^resultados e oportunidades"],
            "Plano de Acao para Implementacao da Agenda Municipal 20230": [r"^plano de acao para implementacao da agenda municipal 20230"],
            "AcoesEixos Tematicos": [r"^acoes", r"^eixos tematicos"],
            "Objetivos Estrategicos": [r"^objetivos estrategicos?"],
            "Metas": [r"^metas$"],
            "Iniciativas": [r"^iniciativas"],
            "Indicador": [r"^indicador$"],
            "Secretarias Responsaveis": [r"^secretarias? responsaveis?"],
            "ODS Vinculado": [r"^ods vinculados?"],
            "Informacoes Complementares": [r"^informacoes complementares"],
            "Contexto": [r"^contexto"],
            "Regionalizacao": [r"^regionalizacao"],
        },
        "ignore": [
            "Pagina",
            "Agenda Municipal 2030",
            "Prefeitura de Sao Paulo",
            "Contextualizacao",
            "Desafios remanescentes",
        ],
        "minimum_font_size": 12,
        "minimum_description_font_size": 10,
    },
}


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


def create_doc_type(blocks, ignore=None, block_names=None, context_name="estruturas"):
    if ignore is None:
        ignore = []

    if block_names is None:
        block_names = []

    return {
        context_name: {
            "blocos": dict(blocks),
            "ignorar": ignore,
            "nomes_blocos": block_names,
        }
    }


def save_json(data, file_name="doc_type.json"):
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    print(f"Arquivo {file_name} criado com sucesso.")


def build_doc_type_from_profile(profile: dict):
    context_name = profile.get("context_name", "estruturas")
    block_names = profile.get("block_names", [])
    rules = profile.get("rules", {})
    minimum_font_size = profile.get("minimum_font_size", 12)
    minimum_description_font_size = profile.get("minimum_description_font_size", 10)

    blocks = []
    for name in block_names:
        blocks.append(
            create_block(
                name,
                match=rules.get(name, [f"^{name.lower()}"]),
                minimum_font_size=minimum_font_size,
                minimum_description_font_size=minimum_description_font_size,
            )
        )

    return create_doc_type(
        blocks,
        ignore=profile.get("ignore", []),
        block_names=block_names,
        context_name=context_name,
    )


def build_doc_type(profile_name="generic_example"):
    if profile_name not in PROFILE_LIBRARY:
        raise ValueError(f"Unknown doc type profile: {profile_name}")

    return build_doc_type_from_profile(PROFILE_LIBRARY[profile_name])
