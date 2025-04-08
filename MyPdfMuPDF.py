import fitz  # PyMuPDF
import json
import os
import re


class MyPdfMuPDF:
    def __init__(self, pdf_path, output_dir, config_path):
        self.pdf_path = pdf_path
        self.output_dir = output_dir
        self.config_path = config_path
        self.ignorar_textos = set()
        self.blocos_config = {}
        self.resultado_final = []
        self.load_config()

    def load_config(self):
        with open(self.config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        self.ignorar_textos = set(config.get("ignorar", []))
        self.blocos_config = config.get("blocos_ODS", {})

    def detectar_bloco(self, texto, fonte):
        for nome_bloco, regras in self.blocos_config.items():
            for pattern in regras.get("match", []):
                if re.match(pattern, texto.lower()) and fonte >= regras.get("descricao_fonte_minima", 0):
                    return nome_bloco
        return None

    def extrair_texto(self):
        doc = fitz.open(self.pdf_path)

        estrutura_atual = None
        bloco_atual = None
        texto_acumulado = ""
        tipo_atual = None

        for pagina_pdf in doc:
            blocos = pagina_pdf.get_text("dict")['blocks']
            for bloco in blocos:
                if 'lines' not in bloco:
                    continue
                for linha in bloco['lines']:
                    spans = linha['spans']
                    
                    if not spans:
                        continue

                    texto_linha = " ".join([span['text'] for span in spans]).strip()
                    fonte = max([span['size'] for span in spans])

                    if texto_linha in self.ignorar_textos or not texto_linha:
                        continue

                    nome_bloco = self.detectar_bloco(texto_linha, fonte)

                    if nome_bloco:
                        # 🟡 Finalizar e armazenar bloco anterior (se existir)
                        if tipo_atual:
                            if bloco_atual:
                                bloco_atual['texto'] = texto_acumulado.strip()
                                if tipo_atual != "ODS" and estrutura_atual is not None:
                                    estrutura_atual['blocos'].append(bloco_atual)
                                bloco_atual = None
                                texto_acumulado = ""

                        # 🔧 Finalizar ODS anterior e adicionar ao resultado
                        if nome_bloco == "ODS":
                            if estrutura_atual:
                                if bloco_atual:
                                    bloco_atual['texto'] = texto_acumulado.strip()
                                    estrutura_atual['blocos'].append(bloco_atual)
                                    bloco_atual = None
                                    texto_acumulado = ""
                                self.resultado_final.append(estrutura_atual)

                            estrutura_atual = {
                                "titulo": texto_linha,
                                "descricao": "",
                                "blocos": []
                            }
                            tipo_atual = "ODS"
                            continue
                        else:
                            bloco_atual = {
                                "tipo": nome_bloco,
                                "titulo": texto_linha,
                                "texto": ""
                            }
                            tipo_atual = nome_bloco
                            texto_acumulado = ""
                            continue

                    # 🔵 Adiciona à descrição da ODS (se for apropriado)
                    if tipo_atual == "ODS" and not nome_bloco and fonte >= self.blocos_config['ODS'].get("descricao_fonte_minima", 12):
                        estrutura_atual['descricao'] += " " + texto_linha
                        continue

                    # 🔵 Continua acumulando texto do bloco atual
                    if tipo_atual and bloco_atual:
                        regras = self.blocos_config.get(tipo_atual, {})
                        fim_ao_conter = regras.get("fim_ao_encontrar", []) 
                        if any(texto_linha.lower().startswith(fim.lower()) for fim in fim_ao_conter) :
                            bloco_atual['texto'] = texto_acumulado.strip()
                            if estrutura_atual:
                                estrutura_atual['blocos'].append(bloco_atual)
                            bloco_atual = None
                            tipo_atual = None
                            texto_acumulado = ""
                            continue

                        texto_acumulado += " " + texto_linha

        # 🟢 Finalizar última estrutura
        if estrutura_atual:
            if bloco_atual:
                bloco_atual['texto'] = texto_acumulado.strip()
                estrutura_atual['blocos'].append(bloco_atual)
            self.resultado_final.append(estrutura_atual)

        self.salvar_jsons_por_ods()

    def salvar_jsons_por_ods(self):
        os.makedirs(self.output_dir, exist_ok=True)
        for i, estrutura in enumerate(self.resultado_final):
            titulo_sanitizado = estrutura['titulo']
            filename = f"{i+1:02d}_{titulo_sanitizado}.json"
            output_path = os.path.join(self.output_dir, filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(estrutura, f, indent=2, ensure_ascii=False)
        print(f"✅ Extração concluída. {len(self.resultado_final)} arquivos salvos em: {self.output_dir}")
