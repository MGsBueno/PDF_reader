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

### Processing Flow

1. Load runtime configuration from `config.json`
2. Load block-detection rules from `doc_type.json`
3. Extract lines from PDFs through the infrastructure extractor
4. Classify lines into logical blocks in the domain layer
5. Persist the final XML output

## Repository Layout

```text
pdf_reader/
  application/
    cleanup_output.py
    compare_outputs.py
    config.py
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

Update `config.json`:

```json
{
  "input_dir": "caminho/para/entrada",
  "output_dir": "caminho/para/saida"
}
```

### 3. Run the main processing flow

```powershell
python -m pdf_reader.entrypoints.process_pdf
```

## CLI Commands

### Process PDFs

```powershell
python -m pdf_reader.entrypoints.process_pdf
```

### Generate `doc_type.json`

```powershell
python -m pdf_reader.entrypoints.generate_doc_type
```

### Compare extraction outputs

```powershell
python -m pdf_reader.entrypoints.compare_outputs
```

### Clean output directory

```powershell
python -m pdf_reader.entrypoints.cleanup_output
```

## Configuration

### `config.json`

Defines runtime input and output directories.

### `doc_type.json`

Defines:

- block names
- regex match rules
- minimum font thresholds
- ignored text prefixes

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
