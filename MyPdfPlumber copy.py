# import pdfplumber
# import json
# import os

# def is_integer(s):
#     try:
#         int(s)  # Tenta converter para inteiro
#         return True
#     except ValueError:
#         return False

# class MyPdfPlumber:
#     def __init__(self, pdf_path, output_dir, config_path):
#         self.pdf_path = pdf_path
#         self.output_dir = output_dir
#         self.config_path = config_path
#         self.ignorar_textos = self.carregar_config()  # Carrega palavras-chave a serem ignoradas

#     def carregar_config(self):
#         """Carrega a lista de textos a serem ignorados do arquivo config.json."""
#         if os.path.exists(self.config_path):
#             with open(self.config_path, "r", encoding="utf-8") as f:
#                 config = json.load(f)
#             return set(config.get("ignorar", []))  # Retorna um conjunto de textos a ignorar
#         return set()
    
#     class Pagina:
#         def __init__(self, numero, largura, altura):
#             self.numero = numero
#             self.largura = largura
#             self.altura = altura
#             self.blocos = []  # Lista para armazenar blocos de título e texto

#         def adicionar_bloco(self, titulo, texto):
#             """Adiciona um novo bloco de título e texto, onde cada bloco é associado ao título."""
#             self.blocos.append({"titulo": titulo, "texto": texto})
        
#         def salvar_como_json(self, output_dir):
#             """Salva os dados da página como JSON."""
#             subpasta = os.path.join(output_dir, "myPdfPlumber")
#             os.makedirs(subpasta, exist_ok=True)

#             json_data = {
#                 "numero": self.numero,
#                 "largura": self.largura,
#                 "altura": self.altura,
#                 "blocos": self.blocos  # Agora armazenamos os blocos de título e texto
#             }

#             # Salvando os dados em UTF-8
#             json_path = os.path.join(subpasta, f"pagina_{self.numero}.json")
#             with open(json_path, 'w', encoding='utf-8') as f:
#                 json.dump(json_data, f, indent=2, ensure_ascii=False)

#     def extrair_texto(self):
#         with pdfplumber.open(self.pdf_path) as pdf:
#             for pagina_pdf in pdf.pages:
#                 pagina = self.Pagina(pagina_pdf.page_number, pagina_pdf.width, pagina_pdf.height)
#                 titulo = ""
#                 texto = ""

#                 words = pagina_pdf.extract_words() 
#                 for word in words:  # word = {'text': 'str', 'x0': float, 'x1': float, 'top': float, 'doctop': float, 'bottom': float, 'upright': boolena, 'height': float, 'width': float, 'direction': 'ltr'}
#                     if word["height"] > 12:  # Se a altura da palavra for maior que 12, ela é parte do título
#                         titulo += " " + word['text'] if titulo else word['text']
#                     else:  # Texto do corpo (quando a altura for menor ou igual a 12)
#                         if texto:
#                             texto += " "
#                         texto += word['text']

#                     # Ignorar cabeçalhos ou números
#                     if texto.strip() in self.ignorar_textos or is_integer(texto.strip()):
#                         texto = ""
#                     else:
#                         pass


#                 #remove numeração de pagina se existir
#                 i = 4
#                 while i > 0:
#                     val = texto[-i:]
#                     pg = str(pagina_pdf.page_number)
#                     if val == pg:
#                         i+=1
#                         texto = texto[:-i]
#                         i = 1  
#                     i -= 1

#                 # Adiciona o bloco com o título e o texto
#                 if texto != "":
#                     pagina.adicionar_bloco(titulo, texto)

#                 pagina.salvar_como_json(self.output_dir)
