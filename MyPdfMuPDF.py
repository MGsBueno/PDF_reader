import fitz  # PyMuPDF
import os
import re
import json
from xml.sax.saxutils import escape

class MyPdfMuPDF:
    def __init__(self, pdf_paths, output_xml_path, doc_type_path):
        """
        pdf_paths: lista de arquivos PDF a serem processados
        output_xml_path: caminho do arquivo XML de saída
        doc_type_path: JSON com configuração dos blocos e ignorar
        """
        self.pdf_paths = pdf_paths
        self.output_xml_path = output_xml_path
        self.doc_type_path = doc_type_path
        self.blocos_config = {}
        self.ignorar_textos = set()
        self.load_config()

    def load_config(self):
        with open(self.doc_type_path, "r", encoding="utf-8") as f:
            doc_type = json.load(f)
        for categoria in doc_type.values():
            if isinstance(categoria, dict) and "blocos" in categoria and "ignorar" in categoria:
                self.blocos_config = categoria.get("blocos", {})
                self.ignorar_textos = set(categoria.get("ignorar", []))
                self.ordem_blocos = list(self.blocos_config.keys())
                break

    def detectar_bloco(self, texto, fonte):
        texto_lower = texto.lower()
        for nome_bloco, regras in self.blocos_config.items():
            for pattern in regras.get("match", []):
                # regex case insensitive com re.IGNORECASE e match desde inicio da linha
                if re.match(pattern, texto_lower, re.IGNORECASE) and fonte >= regras.get("descricao_fonte_minima", 0):
                    return nome_bloco
        return None

    def salvar_entrada_xml(self, nome_bloco, texto):
        """
        Salva um bloco no arquivo XML aberto.
        O nome do bloco é transformado em tag XML (sem espaços).
        """
        tag = nome_bloco.replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_")
        texto_escapado = escape(texto.strip())
        with open(self.output_xml_path, "a", encoding="utf-8") as f:
            f.write(f"  <{tag}>{texto_escapado}</{tag}>\n")

    def processar(self):
        # Abre o arquivo XML e escreve o cabeçalho
        with open(self.output_xml_path, "w", encoding="utf-8") as f:
            f.write("<dados>\n")

        for pdf_path in self.pdf_paths:
            doc = fitz.open(pdf_path)
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

                        is_bold = any('bold' in span.get('font', '').lower() for span in spans)
                        texto_linha = " ".join([span['text'] for span in spans]).strip()
                        fonte = max([span['size'] for span in spans])  # tamanho da fonte

                        texto_linha_lower = texto_linha.lower()
                        if any(texto_linha_lower.startswith(ign.lower()) for ign in self.ignorar_textos):
                            if bloco_atual:
                                self.salvar_entrada_xml(bloco_atual, texto_acumulado.strip())
                                bloco_atual = None
                                texto_acumulado = ""
                                tipo_atual = None
                            continue

                        pode_ser_bloco = (is_bold)
                        nome_bloco = None
                        if pode_ser_bloco:
                            nome_bloco = self.detectar_bloco(texto_linha, fonte)

                        if nome_bloco:
                            # Encontrou início de um novo bloco
                            if bloco_atual:
                                self.salvar_entrada_xml(bloco_atual, texto_acumulado.strip())
                                bloco_atual = None
                                texto_acumulado = ""
                                tipo_atual = None

                            bloco_atual = nome_bloco
                            tipo_atual = nome_bloco
                            texto_acumulado = texto_linha
                        else:
                            if bloco_atual:
                                texto_acumulado += " " + texto_linha

            # Ao final do PDF, se ainda houver bloco em aberto, salvar
            if bloco_atual:
                self.salvar_entrada_xml(bloco_atual, texto_acumulado.strip())
                bloco_atual = None
                texto_acumulado = ""
                tipo_atual = None

        # Fecha o arquivo XML
        with open(self.output_xml_path, "a", encoding="utf-8") as f:
            f.write("</dados>\n")

        print(f"✅ XML final salvo em: {self.output_xml_path}")
