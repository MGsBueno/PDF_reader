# PDF Reader

Structured PDF extraction pipeline for block-based document parsing.

## Overview

`PDF Reader` processes PDF files, detects logical content blocks based on configurable rules, and writes the extracted result to XML.

The current implementation is built around `PyMuPDF` and a layered internal package designed to keep domain rules, application workflows, infrastructure adapters, and CLI entrypoints separated.

## Key Capabilities

- Extract text lines from PDF documents using `PyMuPDF`
- Detect semantic blocks using regex and font-based rules from `doc_type.json`
- Serialize extracted blocks into a consolidated XML output
- Generate default document-type configuration
- Compare outputs across extraction strategies
- Clean generated output artifacts

## Architecture

The project follows a layered package structure:

- `pdf_reader.domain`
  Core models and domain rules
- `pdf_reader.application`
  Use cases and application services
- `pdf_reader.infrastructure`
  Adapters for config loading, PDF extraction, and XML writing
- `pdf_reader.entrypoints`
  CLI-facing entrypoints for local execution

This repository currently uses a layered architecture with a small composition root. The empty legacy `layers/` folder is not part of the runtime design.

### Processing Flow

1. Load runtime configuration from an explicit config file
2. Load block-detection rules from the configured `doc_type.json`
3. Compose concrete adapters in the bootstrap/composition root
4. Extract lines from PDFs through the infrastructure extractor
5. Classify lines into logical blocks in the domain layer
6. Persist the final XML output

## Repository Layout

```text
pdf_reader/
  bootstrap.py
  application/
    cleanup_output.py
    compare_outputs.py
    config.py
    ports.py
    generate_doc_type.py
    process_pdf_batch.py
  domain/
    models.py
    services.py
  entrypoints/
    cleanup_output.py
    compare_outputs.py
    generate_doc_type.py
    process_pdf.py
  infrastructure/
    config_loader.py
    extractors/
      mupdf_block_extractor.py
      pymupdf_extractor.py
    writers/
      xml_writer.py
tests/
.env.example
Algorithm.txt
config.json
doc_type.json
requirements.txt
requirements-dev.txt
```

## Requirements

- Python 3.12+

## Quickstart

### 1. Create a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

### 2. Configure input and output paths

You can configure the project with `config.json`, `.env`, or both.

Example `.env`:

```dotenv
PDF_READER_INPUT_DIR=./input
PDF_READER_OUTPUT_DIR=./output
PDF_READER_OUTPUT_FILE=result.xml
PDF_READER_DOC_TYPE_PATH=./doc_type.json
```

You can start by copying `.env.example` to `.env`.

Then update `config.json` if you want extra settings:

```json
{
  "input_dir": "caminho/para/entrada",
  "output_dir": "caminho/para/saida"
}
```

### 3. Run the main processing flow

```powershell
python -m pdf_reader.entrypoints.process_pdf --config .\config.json
```

## Practical Example

Create a simple local setup like this:

```text
input/
  sample.pdf
output/
config.json
doc_type.json
```

Example `config.json`:

```json
{
  "input_dir": "./input",
  "output_dir": "./output",
  "processing": {
    "output_file": "result.xml",
    "doc_type_path": "./doc_type.json"
  }
}
```

Example `doc_type.json`:

```json
{
  "structures": {
    "blocks": {
      "Title": {
        "match": ["^title"],
        "minimum_description_font_size": 10
      },
      "Summary": {
        "match": ["^summary"],
        "minimum_description_font_size": 10
      }
    },
    "ignore": ["Page", "Footer"]
  }
}
```

Run:

```powershell
python -m pdf_reader.entrypoints.process_pdf --config .\config.json
```

Expected output file:

```text
output/result.xml
```

Example output:

```xml
<data>
  <Title>Document title</Title>
  <Summary>Consolidated summary of the extracted content</Summary>
</data>
```

## CLI Commands

### Process PDFs

```powershell
python -m pdf_reader.entrypoints.process_pdf --config .\config.json
```

### Generate `doc_type.json`

```powershell
python -m pdf_reader.entrypoints.generate_doc_type --config .\config.json
```

### Compare extraction outputs

```powershell
python -m pdf_reader.entrypoints.compare_outputs --config .\config.json
```

### Clean output directory

```powershell
python -m pdf_reader.entrypoints.cleanup_output --config .\config.json
```

## Configuration

### `config.json`

Defines runtime input and output directories. Relative paths are resolved from the directory that contains the chosen config file.

### `.env`

If a `.env` file exists in the same directory as `config.json`, it is loaded automatically before the runtime config is built.

Supported variables:

- `PDF_READER_INPUT_DIR`
- `PDF_READER_OUTPUT_DIR`
- `PDF_READER_OUTPUT_FILE`
- `PDF_READER_DOC_TYPE_PATH`
- `PDF_READER_COMPARISON_OUTPUT_FILE`
- `PDF_READER_DOC_TYPE_PROFILE`
- `PDF_READER_DOC_TYPE_OUTPUT_PATH`

You can also reference environment variables inside `config.json` with `${VAR_NAME}` syntax.

### `doc_type.json`

Defines:

- block names
- regex match rules
- minimum font thresholds
- ignored text prefixes

The supported schema is now strict and uses the English keys `structures`, `blocks`, `ignore`, and `minimum_description_font_size`.

### Legacy compatibility

`MuPdfBlockExtractor` is kept only as a legacy compatibility wrapper. New integrations should use the main `PdfBatchProcessor` flow through the composition root in `pdf_reader/bootstrap.py`.

## Development

### Run tests

```powershell
python -m pytest -q tests
```

### Install runtime dependencies only

```powershell
pip install -r requirements.txt
```

## Status

This repository is currently in pre-release and the internal architecture is still evolving. The public structure should be considered unstable until the first stable release.
