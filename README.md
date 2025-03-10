# PDF Reader - Processamento de PDFs com Diferentes Métodos

## Descrição

Este projeto permite a extração de texto de arquivos PDF. Na primeira etapa utiliza diferentes bibliotecas de processamento em Python. Atualmente utilizando PdfPlumber, PyMuPDF e PdfMiner gera resultados de forma estruturada e compara seus tempos de execuçao no prompt.

## Estrutura dos Arquivos

### Scripts Principais

- **`valida.py`**: Script responsável pela comparação dos PDFs processados.
- **`Save.py`**: Gerencia o salvamento dos resultados extraídos.
- **`delete.py`**: Script responsável por limpar o diretorio de saída.

### Métodos de Extração

- **`MyPdfPlumber.py`**: Implementação do método de extração usando a biblioteca PdfPlumber.
- **`MyPdfMuPDF.py`**: Implementação do método de extração usando a biblioteca PyMuPDF.
- **`MyPdfMiner.py`**: Implementação do método de extração usando a biblioteca PdfMiner.

### Arquivos Auxiliares

- **`algoritmo.txt`**: Documento contendo o fluxo ou explicação do algoritmo utilizado.
- **`config.json`**: Arquivo de configuração que define diretórios de entrada e saída.

## Como Usar

1. **Configurar o ambiente:**

   - Certifique-se de ter o Python instalado em sua máquina.
   - Instale as bibliotecas necessárias executando:

     ```bash
     pip install pdfplumber pymupdf pdfminer.six
     ```

2. **Configurar os diretórios:**

   - Edite o arquivo `config.json` para definir os caminhos de entrada e saída:

     ```json
     {
       "input_dir": "caminho/para/diretorio/de/entrada",
       "output_dir": "caminho/para/diretorio/de/saida"
     }
     ```

3. **Executar o processamento:**

   - Execute o script principal que faz a chamada dos métodos desejados:

     ```bash
     python save.py
     ```

   - Os resultados serão armazenados em diretórios organizados pelo nome de cada arquivo e internamente por método de extração.

## Dependências

Certifique-se de instalar as bibliotecas necessárias antes de executar os scripts:

```bash
pip install pdfplumber pymupdf pdfminer.six
```
