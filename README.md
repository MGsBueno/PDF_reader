# PDF Batch Extractor

Structured PDF extraction pipeline for block-based document parsing.

This project provides a configurable and extensible system to extract structured data from PDFs and transform it into XML using a block-based approach.

---

## Features

- Block-based PDF parsing using **PyMuPDF**
- Configurable extraction via `doc_type.json`
- XML output generation
- CLI-based execution
- Layered architecture (domain, application, infrastructure)
- Composition root for dependency wiring
- Automated tests with `pytest`
- Code quality enforcement:
  - `black` (formatting)
  - `flake8` (linting)
  - `mypy` (type checking)
- CI pipeline with GitHub Actions

---

## Architecture

The project follows a **layered architecture**:

```text
pdf_batch_extractor/
  domain/           # Core models and business rules
  application/      # Use cases and orchestration
  infrastructure/   # External adapters (PDF, config, XML)
  entrypoints/      # CLI interfaces
  bootstrap.py      # Composition root
```

### Design Principles

- Separation of concerns
- Dependency inversion via ports
- Config-driven behavior
- Testable components

---

## Installation

### Option 1 - Editable (recommended for development)

```bash
pip install -e .
```

### Option 2 - Standard

```bash
pip install .
```

---

## Development Setup

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -e .
```

---

## Usage

### Process PDFs

```bash
pdf-batch-extractor --config config.json
```

### Generate document type configuration

```bash
pdf-batch-extractor-generate-doc-type
```

### Compare outputs

```bash
pdf-batch-extractor-compare-outputs
```

### Cleanup output directory

```bash
pdf-batch-extractor-cleanup-output
```

---

## Configuration

### `config.json`

Controls runtime behavior:

```json
{
  "input_dir": "./input",
  "output_dir": "./output",
  "processing": {
    "output_file": "result.xml",
    "doc_type_path": "doc_type.json"
  }
}
```

---

### `doc_type.json`

Defines how blocks are extracted:

```json
{
  "structures": {
    "blocks": {
      "Title": {
        "match": ["^Title"],
        "minimum_description_font_size": 12
      }
    },
    "ignore": ["Page", "Header", "Footer"]
  }
}
```

---

## Testing

```bash
pytest -q
```

---

## Code Quality

```bash
flake8 .
black --check .
mypy .
```

---

## CI Pipeline

The project uses GitHub Actions to ensure:

- Tests execution
- Code formatting validation
- Linting checks
- Static type checking

All checks must pass before merging into `main`.

---

## Example Flow

```text
PDF input -> Line extraction -> Block detection -> XML output
```

---

## Project Status

**Development Status:** Pre-Alpha

The project is under active development and subject to changes.

---

## Motivation

This project was designed to:

- Explore clean architecture in Python
- Build a configurable document parsing system
- Improve maintainability and extensibility of PDF extraction pipelines

---

## License

MIT License

