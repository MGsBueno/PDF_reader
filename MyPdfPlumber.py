import pdfplumber
import json
import os
import statistics

class MyPdfPlumber:
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
            subpasta = os.path.join(output_dir, "myPdfPlumber")
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
        with pdfplumber.open(self.pdf_path) as pdf:
            titulo_anterior = ""
            titulo_tam_anterior = 0
            for pagina_pdf in pdf.pages:
                pagina = self.Pagina(pagina_pdf.page_number, pagina_pdf.width, pagina_pdf.height)
                bottom = -1
                tamanho_anterior = 14
                titulo_acumulado = []
                texto_atual_bloco = []
                font_sizes_texto = []
                font_size_titulo = 0
                titulo_atual = ""
                linha_atual = ""
            
               
                palavras = pagina_pdf.extract_words()
                for palavra in palavras:
                    if palavra["height"] >= 12 and tamanho_anterior >= 12:
                        titulo_acumulado.append(palavra["text"])
                        titulo_tam_anterior = palavra["height"]
                        font_size_titulo = titulo_tam_anterior

                    elif palavra["height"] > 12 and tamanho_anterior < 12:
                        tamanho_anterior = font_size_titulo
                        if( titulo_atual == "" and texto_atual_bloco != []):
                            for str_palavra in titulo_acumulado: titulo_atual += str_palavra + " "
                            font_size_titulo = palavra["height"]
                            media_fonte = round(statistics.mean(font_sizes_texto), 1)
                            titulo_fonte = round(statistics.mean(font_size_titulo), 1)
                            titulo_anterior = titulo_atual.strip()
                            pagina.adicionar_bloco(titulo_anterior, texto_atual_bloco, titulo_fonte, media_fonte)  
            

                    elif (palavra["height"] < 12 and round(float(palavra["bottom"]), 2) - bottom < 2):
                        font_sizes_texto.append(palavra["height"])
                        linha_atual+= " " + palavra["text"]
                        if (linha_atual in self.ignorar_textos) or (linha_atual == pagina_pdf.page_number):
                            linha_atual = ""
                    elif palavra["height"]<12:
                        if linha_atual != "":
                            texto_atual_bloco.append(linha_atual)
                        linha_atual = palavra['text']
                        bottom = round(float(palavra["bottom"]), 2)
                
                if font_sizes_texto:
                    media_fonte = round(statistics.mean(font_sizes_texto), 1)
                else: media_fonte = 0


                if( titulo_atual == "" and titulo_acumulado != []):
                    for str_palavra in titulo_acumulado: titulo_atual += str_palavra + " "
                    font_size_titulo = tamanho_anterior
                    titulo_anterior = titulo_atual.strip()
                
                if( titulo_atual == "" and titulo_acumulado == [] and texto_atual_bloco != []):
                    titulo_atual = titulo_anterior
                                    
                titulo_fonte = round(font_size_titulo, 1)
                
                pagina.adicionar_bloco(titulo_atual.strip(),texto_atual_bloco, titulo_fonte, media_fonte)  
                pagina.salvar_como_json(self.output_dir)

                            
