import fitz  # PyMuPDF
import json
import os
import statistics

class MyPdfMuPDF:
    def __init__(self, pdf_path, output_dir, config_path):
        self.pdf_path = pdf_path
        self.output_dir = output_dir
        self.config_path = config_path
        self.ignorar_textos, self.tratar_textos = self.carregar_config()

    def carregar_config(self):
        """Carrega as configurações de textos a ignorar e tratar."""
        if os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            return set(config.get("ignorar", [])), set(config.get("tratar", []))
        return set(), set()

    class Pagina:
        def __init__(self, numero, largura, altura):
            self.numero = numero
            self.largura = largura
            self.altura = altura
            self.blocos = []

        def adicionar_bloco(self, titulo, texto, font_size_titulo, font_size_media_texto):
            """Adiciona um bloco de conteúdo à página."""
            self.blocos.append({
                "titulo": titulo,
                "texto": texto,
                "font_size_titulo": font_size_titulo,
                "font_size_media_texto": font_size_media_texto
            })

        def salvar_como_json(self, output_dir):
            """Salva a página como JSON."""
            subpasta = os.path.join(output_dir, "myPdfMuPDF")
            os.makedirs(subpasta, exist_ok=True)
            
            json_data = {
                "numero": self.numero,
                "largura": self.largura,
                "altura": self.altura,
                "blocos": self.blocos
            }

            json_path = os.path.join(subpasta, f"pagina_{self.numero}.json")
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)

    def extrair_texto(self):
        doc = fitz.open(self.pdf_path)
        
        titulo_anterior = ""
        
        for pagina_pdf in doc:
            pagina = self.Pagina(pagina_pdf.number + 1, pagina_pdf.rect.width, pagina_pdf.rect.height)
            titulo_acumulado = []
            texto_atual_bloco = []
            font_sizes_texto = []
            font_size_titulo = 0
            titulo_atual = ""

            linhas = pagina_pdf.get_text("dict")["blocks"]

            for bloco in linhas:
                if "lines" in bloco:
                    for linha in bloco["lines"]:
                        linha_texto = " ".join(span["text"].strip() for span in linha["spans"])
                        font_size = linha["spans"][0]["size"]

                        # Ignorar textos e números de página
                        if linha_texto in self.ignorar_textos or linha_texto.isdigit():
                            continue

                        # Identificar títulos
                        if font_size > 12:
                            titulo_acumulado.append(linha_texto)
                            font_size_titulo = font_size
                        else:
                            texto_atual_bloco.append(linha_texto)
                            font_sizes_texto.append(font_size)

            titulo_atual = " ".join(titulo_acumulado)
            if titulo_atual != "":
               titulo_anterior =  titulo_atual
            font_size_media_texto = statistics.mean(font_sizes_texto) if font_sizes_texto else 0
            if (titulo_atual == "" and texto_atual_bloco):
                titulo_atual = titulo_anterior
            if titulo_atual and texto_atual_bloco:
                pagina.adicionar_bloco(titulo_atual, texto_atual_bloco, font_size_titulo, int(font_size_media_texto))
            pagina.salvar_como_json(self.output_dir)
