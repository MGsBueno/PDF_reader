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

def criar_doc_type(blocos, ignorar=None, nomes_blocos=None):
    if ignorar is None:
        ignorar = []
    
    if nomes_blocos is None:
        nomes_blocos = []
    
    return {
        "estruturas": {
            "blocos": dict(blocos),
            "ignorar": ignorar,
            "nomes_blocos" : nomes_blocos
        }
    }

def salvar_json(data, nome_arquivo='doc_type.json'):
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Arquivo {nome_arquivo} criado com sucesso.")

if __name__ == "__main__":
    nomes_blocos = [
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
        "Regionalização"
    ]

    # Lista global que define os textos que indicam fim de qualquer bloco
    lista_fim_ao_encontrar = nomes_blocos

    blocos = []
    for nome in nomes_blocos:
        # Define regexs específicas conforme seu código anterior
        pattern = [f"^{nome.lower()}"]

        if nome == "Objetivo de Desenvolvimento Estratégico (ODS)":
            pattern = [r"^(ods|objetivo de desenvolvimento estratégico\s*\(?ods\)?)"]
        elif nome == "Meta Global":
            pattern = [r"^meta global"]
        elif nome == "Meta Municipal":
            pattern = [r"^meta municipal"]
        elif nome == "Contextualização":
            pattern = [r"^contextualização"]
        elif nome == "Indicadores":
            pattern = [r"^indicadores", r"^indicadores priorizados"]
        elif nome == "Desafios Remanescentes":
            pattern = [r"^desafios remanescentes"]
        elif nome == "Classificação de Governabilidade":
            pattern = [r"^classificação de governabilidade"]
        elif nome == "Resultados e Oportunidaddes":
            pattern = [r"^resultados e oportunidades"]
        elif nome == "Plano de Ação para Implementação da Agenda Municipal 20230":
            pattern = [r"^plano de ação para implementação da agenda municipal 20230"]
        elif nome == "AçõesEixos Temáticos":
            pattern = [r"^ações", r"^eixos temáticos"]
        elif nome == "Objetivos Estratégicos":
            pattern = [r"^objetivos estratégicos?"]
        elif nome == "Metas":
            pattern = [r"^metas$"]
        elif nome == "Iniciativas":
            pattern = [r"^iniciativas"]
        elif nome == "Indicador":
            pattern = [r"^indicador$"]
        elif nome == "Secretarias Responsáveis":
            pattern = [r"^secretarias? responsáveis?"]
        elif nome == "ODS Vinculado":
            pattern = [r"^ods vinculados?"]
        elif nome == "Informações Complementares":
            pattern = [r"^informações complementares"]
        elif nome == "Contexto":
            pattern = [r"^contexto"]
        elif nome == "Regionalização":
            pattern = [r"^regionalização"]

        fonte_minima = 12
        descricao_fonte_minima = 10
        
        blocos.append(criar_bloco(
            nome,
            match=pattern,
            fonte_minima=fonte_minima,
            descricao_fonte_minima=descricao_fonte_minima,
        ))

    ignorar = [
        "Página",
        "Agenda Municipal 2030",
        "Prefeitura de São Paulo",
        "Contextualização",
        "Desafios remanescentes"
    ]


    doc_type = criar_doc_type(blocos, ignorar, nomes_blocos)
    salvar_json(doc_type)
