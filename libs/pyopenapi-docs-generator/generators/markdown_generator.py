#!/usr/bin/env python3
"""
Markdown documentation generator for OpenAPI schemas.
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any


class MarkdownGenerator:
    """Generates Markdown documentation from OpenAPI schemas."""
    
    def __init__(self, output_dir: str = "docs/md"):
        """
        Initialize the Markdown generator.
        
        Args:
            output_dir: Directory where Markdown files will be saved
        """
        self.output_dir = Path(output_dir)
        self._ensure_output_directory()
    
    def _ensure_output_directory(self) -> Path:
        """Ensure the output directory exists and return its absolute path."""
        abs_output_dir = self.output_dir.resolve()
        abs_output_dir.mkdir(parents=True, exist_ok=True)
        return abs_output_dir
    
    def _generate_header(self, service_name: str) -> str:
        """Generate a standard Markdown header with service info."""
        return f"""# {service_name} API Documentation

**Generated on**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

"""
    
    def _process_schema(self, schema_name: str, schema_data: Dict[str, Any]) -> str:
        """Generate formatted Markdown documentation for a single JSON Schema."""
        display_name = schema_name.replace("Get", "").replace("ResponseContent", "")
        content = f"## Component Schema: `{display_name}`\n\n"
        
        # Type and description
        if 'type' in schema_data:
            content += f"- **Type**: `{schema_data['type']}`\n"
        
        if 'description' in schema_data:
            content += f"- **Description**: {schema_data['description']}\n"
        
        # Properties
        if 'properties' in schema_data:
            content += "\n### Properties:\n\n"
            for prop_name, prop_data in schema_data['properties'].items():
                content += f"- **`{prop_name}`**\n"
                
                if '$ref' in prop_data:
                    content += f"  - `$ref`: {prop_data['$ref']}\n"
                else:
                    if 'type' in prop_data:
                        content += f"  - **Type**: `{prop_data['type']}`\n"
                    if 'description' in prop_data:
                        content += f"  - **Description**: {prop_data['description']}\n"
                    if 'enum' in prop_data:
                        content += f"  - **Enum values**: `{', '.join(prop_data['enum'])}`\n"
        
        # Enum (for schemas that are only enums)
        if 'enum' in schema_data and 'properties' not in schema_data:
            content += "\n### Enum values:\n\n"
            content += f"`{', '.join(str(item) for item in schema_data['enum'])}`\n"
        
        # Required fields
        if 'required' in schema_data:
            content += "\n### Required properties:\n\n"
            content += f"`{', '.join(schema_data['required'])}`\n"
        
        content += "\n---\n\n"
        return content
    
    def _generate_filename(self, service_name: str) -> str:
        """Generate output filename based on service name."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{service_name.lower()}_{timestamp}.md"
    
    def generate_from_spec(self, spec_data: Dict[str, Any], service_name: str) -> str:
        """
        Generate Markdown documentation from OpenAPI specification.
        
        Args:
            spec_data: OpenAPI specification data
            service_name: Name of the service
            
        Returns:
            Path to generated Markdown file
        """
        # Start Markdown content
        md_content = self._generate_header(service_name)
        
        # Add API info
        if 'info' in spec_data:
            info = spec_data['info']
            md_content += f"**Title**: {info.get('title', 'N/A')}\n"
            md_content += f"**Version**: {info.get('version', 'N/A')}\n"
            if 'description' in info:
                md_content += f"**Description**: {info['description']}\n"
            md_content += "\n---\n\n"
        
        # Check if components and schemas exist
        if 'components' not in spec_data or 'schemas' not in spec_data['components']:
            md_content += "No component schemas found in the OpenAPI file.\n"
        else:
            schemas = spec_data['components']['schemas']
            total_schemas = len(schemas)
            md_content += f"**Total Schemas Found**: {total_schemas}\n\n---\n\n"
            
            # Process each schema
            for schema_name, schema_data in schemas.items():
                md_content += self._process_schema(schema_name, schema_data)
        
        # Generate output path
        output_filename = self._generate_filename(service_name)
        output_path = self.output_dir / output_filename
        
        # Save Markdown file
        with open(output_path, 'w', encoding='utf-8') as md_file:
            md_file.write(md_content)
        
        print(f"Markdown file generated: {output_path}")
        return str(output_path)