# OpenAPI Documentation Generator

A lightweight Python library for generating documentation from OpenAPI specifications in multiple formats.

## Features

- **Multiple Output Formats**: PlantUML diagrams, Markdown, PDF, and plain text
- **Smithy Integration**: Reads OpenAPI specs from Smithy build outputs
- **Batch Processing**: Generate docs for all services or specific services
- **Clean Architecture**: Modular design with separate generators for each format

## Installation

```bash
# Optional: Install ReportLab for PDF generation
pip install reportlab
```

## Usage

### Command Line

```bash
# Generate all formats for all services
python main.py

# Generate specific formats
python main.py --formats puml md

# Generate for specific service
python main.py --service UserService --formats md pdf

# Custom directories
python main.py --build-dir custom/build --output-dir custom/docs
```

### Python API

```python
from core.docs_generator import DocsGenerator

# Initialize generator
generator = DocsGenerator("build/smithy", "docs")

# Generate all formats for all services
generated_files = generator.generate_all_docs()

# Generate specific formats for specific service
generated_files = generator.generate_for_service("UserService", ["puml", "md"])
```

## Directory Structure

```
libs/openapi-docs-generator/
├── core/
│   ├── docs_generator.py      # Main orchestrator
│   └── openapi_processor.py   # OpenAPI spec loader
├── generators/
│   ├── puml_generator.py      # PlantUML diagrams
│   ├── markdown_generator.py  # Markdown documentation
│   ├── pdf_generator.py       # PDF generation
│   └── txt_generator.py       # Plain text output
├── main.py                    # CLI entry point
└── README.md
```

## Input Structure

The generator expects OpenAPI specifications in the following structure:

```
build/smithy/
├── back-ms-users/
│   └── openapi/
│       └── UserService.openapi.json
├── back-ms-movies/
│   └── openapi/
│       └── MovieService.openapi.json
└── ...
```

## Output Structure

Generated documentation is organized by format:

```
docs/
├── puml/
│   ├── userservice_20241104_143022.puml
│   └── movieservice_20241104_143023.puml
├── md/
│   ├── userservice_20241104_143022.md
│   └── movieservice_20241104_143023.md
├── pdf/
│   ├── userservice_20241104_143022.pdf
│   └── movieservice_20241104_143023.pdf
└── txt/
    ├── userservice_20241104_143022.txt
    └── movieservice_20241104_143023.txt
```

## Generated Content

### PlantUML Diagrams
- Class diagrams showing schema relationships
- Enum definitions
- Property types and requirements
- Visualizable at https://www.planttext.com/

### Markdown Documentation
- Service information and descriptions
- Schema definitions with properties
- Required fields and data types
- Enum values and constraints

### PDF Documentation
- Professional formatted documentation
- Service overview and schema details
- Fallback to text format if ReportLab unavailable

### Text Documentation
- Plain text format for easy reading
- API endpoints and operations
- Complete schema information
- Cross-platform compatible

## Dependencies

- **Python 3.6+**
- **ReportLab** (optional, for PDF generation)

## Error Handling

- Graceful handling of missing OpenAPI files
- Fallback text generation when PDF libraries unavailable
- Individual format error isolation
- Detailed error messages and logging