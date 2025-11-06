"""
OpenAPI Documentation Generator

A lightweight library for generating documentation from OpenAPI specifications
in multiple formats (PlantUML, Markdown, PDF, Text).
"""

from .core.docs_generator import DocsGenerator
from .core.openapi_processor import OpenApiProcessor
from .generators.puml_generator import PumlGenerator
from .generators.markdown_generator import MarkdownGenerator
from .generators.pdf_generator import PdfGenerator
from .generators.txt_generator import TxtGenerator

__version__ = "1.0.0"
__all__ = [
    "DocsGenerator",
    "OpenApiProcessor", 
    "PumlGenerator",
    "MarkdownGenerator",
    "PdfGenerator",
    "TxtGenerator"
]