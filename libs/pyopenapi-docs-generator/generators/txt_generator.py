#!/usr/bin/env python3
"""
Text documentation generator for OpenAPI schemas.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, Any


class TxtGenerator:
    """Generates plain text documentation from OpenAPI schemas."""
    
    def __init__(self, output_dir: str = "docs/txt"):
        """
        Initialize the text generator.
        
        Args:
            output_dir: Directory where text files will be saved
        """
        self.output_dir = Path(output_dir)
        self._ensure_output_directory()
    
    def _ensure_output_directory(self) -> Path:
        """Ensure the output directory exists and return its absolute path."""
        abs_output_dir = self.output_dir.resolve()
        abs_output_dir.mkdir(parents=True, exist_ok=True)
        return abs_output_dir
    
    def _generate_filename(self, service_name: str) -> str:
        """Generate output filename based on service name."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{service_name.lower()}_{timestamp}.txt"
    
    def generate_from_spec(self, spec_data: Dict[str, Any], service_name: str) -> str:
        """
        Generate text documentation from OpenAPI specification.
        
        Args:
            spec_data: OpenAPI specification data
            service_name: Name of the service
            
        Returns:
            Path to generated text file
        """
        content = f"{service_name} API Documentation\n"
        content += "=" * (len(service_name) + 20) + "\n\n"
        content += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # API info
        if 'info' in spec_data:
            info = spec_data['info']
            content += "API INFORMATION\n"
            content += "-" * 15 + "\n"
            content += f"Title: {info.get('title', 'N/A')}\n"
            content += f"Version: {info.get('version', 'N/A')}\n"
            if 'description' in info:
                content += f"Description: {info['description']}\n"
            content += "\n"
        
        # Paths/Operations
        if 'paths' in spec_data:
            content += "API ENDPOINTS\n"
            content += "-" * 13 + "\n"
            for path, methods in spec_data['paths'].items():
                content += f"Path: {path}\n"
                for method, operation in methods.items():
                    content += f"  {method.upper()}:\n"
                    if 'operationId' in operation:
                        content += f"    Operation ID: {operation['operationId']}\n"
                    if 'description' in operation:
                        content += f"    Description: {operation['description']}\n"
                    if 'parameters' in operation:
                        content += "    Parameters:\n"
                        for param in operation['parameters']:
                            content += f"      - {param.get('name', 'N/A')} ({param.get('in', 'N/A')})\n"
                content += "\n"
        
        # Schemas
        if 'components' in spec_data and 'schemas' in spec_data['components']:
            schemas = spec_data['components']['schemas']
            content += "COMPONENT SCHEMAS\n"
            content += "-" * 17 + "\n"
            content += f"Total schemas: {len(schemas)}\n\n"
            
            for schema_name, schema_data in schemas.items():
                content += f"Schema: {schema_name}\n"
                
                if 'type' in schema_data:
                    content += f"  Type: {schema_data['type']}\n"
                
                if 'description' in schema_data:
                    content += f"  Description: {schema_data['description']}\n"
                
                if 'properties' in schema_data:
                    content += "  Properties:\n"
                    required_props = schema_data.get('required', [])
                    for prop_name, prop_data in schema_data['properties'].items():
                        prop_type = prop_data.get('type', 'Unknown')
                        if '$ref' in prop_data:
                            prop_type = prop_data['$ref'].split('/')[-1]
                        required_marker = " (required)" if prop_name in required_props else ""
                        content += f"    - {prop_name}: {prop_type}{required_marker}\n"
                        if 'description' in prop_data:
                            content += f"      Description: {prop_data['description']}\n"
                
                if 'enum' in schema_data and 'properties' not in schema_data:
                    enum_values = ', '.join(str(v) for v in schema_data['enum'])
                    content += f"  Enum values: {enum_values}\n"
                
                if 'required' in schema_data and 'properties' in schema_data:
                    content += f"  Required fields: {', '.join(schema_data['required'])}\n"
                
                content += "\n"
        
        # Generate output path
        output_filename = self._generate_filename(service_name)
        output_path = self.output_dir / output_filename
        
        # Save text file
        with open(output_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(content)
        
        print(f"Text file generated: {output_path}")
        return str(output_path)