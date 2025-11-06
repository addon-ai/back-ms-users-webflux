#!/usr/bin/env python3
"""
OpenAPI processor for loading and processing OpenAPI specifications.
"""

import json
from pathlib import Path
from typing import Dict, Any, List


class OpenApiProcessor:
    """Processes OpenAPI specifications from build directory."""
    
    def __init__(self, build_dir: str = "build/smithy"):
        """
        Initialize the OpenAPI processor.
        
        Args:
            build_dir: Directory containing Smithy build outputs
        """
        self.build_dir = Path(build_dir)
    
    def load_openapi_specs(self) -> List[Dict[str, Any]]:
        """
        Load all OpenAPI specifications from the schemas directory.
        
        Returns:
            List of OpenAPI specifications with metadata
        """
        specs = []
        
        if not self.build_dir.exists():
            print(f"Schemas directory not found: {self.build_dir}")
            return specs
        
        # Check for all_schemas.json first
        all_schemas_file = self.build_dir / "all_schemas.json"
        if all_schemas_file.exists():
            try:
                with open(all_schemas_file, 'r', encoding='utf-8') as f:
                    all_schemas = json.load(f)
                
                # Group schemas by service
                services = {}
                for schema_key, schema_data in all_schemas.items():
                    if '_' in schema_key:
                        service_name = schema_key.split('_')[0]
                        if service_name not in services:
                            services[service_name] = {'components': {'schemas': {}}}
                        
                        # Extract schema name (remove service prefix)
                        schema_name = '_'.join(schema_key.split('_')[1:])
                        services[service_name]['components']['schemas'][schema_name] = schema_data
                
                # Create specs for each service
                for service_name, service_data in services.items():
                    specs.append({
                        'file_path': str(all_schemas_file),
                        'project_name': service_name,
                        'service_name': service_name,
                        'spec': service_data
                    })
                    print(f"Loaded schemas for service: {service_name}")
                    
            except Exception as e:
                print(f"Error loading {all_schemas_file}: {e}")
        else:
            # Fallback: look for individual project directories
            for project_dir in self.build_dir.iterdir():
                if project_dir.is_dir() and not project_dir.name.startswith('.'):
                    # Create a mock OpenAPI spec from individual schema files
                    schemas = {}
                    for schema_file in project_dir.glob("*.json"):
                        if not schema_file.name.startswith('fake-data'):
                            try:
                                with open(schema_file, 'r', encoding='utf-8') as f:
                                    schema_data = json.load(f)
                                schemas[schema_file.stem] = schema_data
                            except Exception as e:
                                print(f"Error loading {schema_file}: {e}")
                    
                    if schemas:
                        specs.append({
                            'file_path': str(project_dir),
                            'project_name': project_dir.name,
                            'service_name': project_dir.name,
                            'spec': {'components': {'schemas': schemas}}
                        })
                        print(f"Loaded schemas for project: {project_dir.name}")
        
        return specs
    
    def get_spec_by_service(self, service_name: str) -> Dict[str, Any]:
        """
        Get OpenAPI specification by service name.
        
        Args:
            service_name: Name of the service
            
        Returns:
            OpenAPI specification data
        """
        specs = self.load_openapi_specs()
        for spec in specs:
            if spec['service_name'] == service_name:
                return spec
        return {}