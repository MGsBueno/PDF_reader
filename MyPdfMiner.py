from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTTextLineHorizontal
import json
import os

class MyPdfMiner:
    def __init__(self, pdf_path, output_dir, config_path):
        self.pdf_path = pdf_path
        self.output_dir = output_dir
        self.config_path = config_path
        self.ignorar_textos = self.carregar_config()
        self.titulo_anterior = ""  # Para armazenar o título da página anterior

    def carregar_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            return set(config.get("ignorar", []))
        return set()

    class Pagina:
        def __init__(self, numero, largura, altura):
            self.numero = numero
            self.largura = largura
            self.altura = altura
            self.blocos = []

        def adicionar_bloco(self, titulo, texto, font_size_titulo, font_size_media_texto):
            self.blocos.append({
                "titulo": titulo,
                "texto": texto,
                "font_size_titulo": font_size_titulo,
                "font_size_media_texto": font_size_media_texto
            })

        def salvar_como_json(self, output_dir):
            subpasta = os.path.join(output_dir, "myPdfMiner")
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
        with open(self.pdf_path, "rb") as f:
            for page_layout in extract_pages(f):
                largura = page_layout.width
                altura = page_layout.height
                pagina = self.Pagina(page_layout.pageid, largura, altura)

                titulo_atual = ""  # Se não tiver título na página, título fica vazio
                texto_atual_bloco = []
                font_sizes_texto = []
                font_size_titulo = 0
                titulo_acumulado = []  # Para acumular as linhas do título
                tem_texto = False  # Variável para verificar se há texto na página

                for element in page_layout:
                    if isinstance(element, LTTextContainer):
                        for text_line in element:
                            if isinstance(text_line, LTTextLineHorizontal):
                                texto = text_line.get_text().strip()
                                font_size = text_line.height

                                # Ignorar se o texto estiver na lista de ignorar ou for apenas números
                                if texto in self.ignorar_textos or texto.isdigit():
                                    continue

                                # Se a fonte for maior ou igual a 12, trata-se de título
                                if font_size >= 12:
                                    # Se já houver título acumulado, significa que o título está em mais de uma linha
                                    if titulo_acumulado:
                                        # Se a linha de título atual é seguida de outra, concatene ao título acumulado
                                        titulo_acumulado.append(texto)
                                    else:
                                        # Caso contrário, inicie um novo título
                                        titulo_acumulado = [texto]
                                    font_size_titulo = font_size
                                    texto_atual_bloco = []  # Resetar o bloco de texto
                                    font_sizes_texto = []  # Resetar as fontes do texto
                                    tem_texto = True  # Indicar que há texto
                                else:
                                    # Adicionar o texto ao bloco atual
                                    texto_atual_bloco.append(texto)
                                    font_sizes_texto.append(font_size)
                                    tem_texto = True  # Indicar que há texto

                # Salvar o último bloco com a média de font_size do texto
                if titulo_acumulado:
                    titulo_completo = " ".join(titulo_acumulado)  # Concatenar as linhas do título
                    font_size_media_texto = sum(font_sizes_texto) / len(font_sizes_texto) if font_sizes_texto else 0
                    pagina.adicionar_bloco(titulo_completo, texto_atual_bloco, font_size_titulo, font_size_media_texto)
                elif tem_texto:
                    # Caso não tenha título, mas tenha texto, atribuir título vazio e herdar o título da página anterior
                    if self.titulo_anterior:
                        titulo_atual = self.titulo_anterior
                    font_size_media_texto = sum(font_sizes_texto) / len(font_sizes_texto) if font_sizes_texto else 0
                    pagina.adicionar_bloco(titulo_atual, texto_atual_bloco, 0, font_size_media_texto)

                pagina.salvar_como_json(self.output_dir)

                # Atualizar o título anterior para a próxima página, somente se houver título ou texto
                if tem_texto and titulo_acumulado:
                    self.titulo_anterior = " ".join(titulo_acumulado)  # Atualiza com o título completo da página atual
                elif tem_texto and not titulo_acumulado:
                    # Caso não tenha título, mas tenha texto, herdar título da página anterior
                    self.titulo_anterior = self.titulo_anterior

