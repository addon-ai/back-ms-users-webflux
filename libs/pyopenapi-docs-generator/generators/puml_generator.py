#!/usr/bin/env python3
"""
PlantUML diagram generator for OpenAPI schemas.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Set, Tuple


class PumlGenerator:
    """Generates PlantUML diagrams from OpenAPI schemas."""
    
    def __init__(self, output_dir: str = "docs/puml/open-api"):
        """
        Initialize the PlantUML generator.
        
        Args:
            output_dir: Directory where PUML files will be saved
        """
        self.output_dir = Path(output_dir)
        self._ensure_output_directory()
    
    def _ensure_output_directory(self) -> Path:
        """Ensure the output directory exists and return its absolute path."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"Created output directory: {self.output_dir.absolute()}")
        return self.output_dir.absolute()
    
    def _generate_header(self, model_name: str = "Visual Model") -> str:
        """Generate PlantUML header with styling."""
        return f"""'This diagram can be visualized at: https://www.planttext.com/

@startuml {model_name}
skinparam defaultFontName Arial
skinparam defaultFontSize 10
skinparam componentStyle uml2
skinparam linetype curved

"""
    
    def _process_enum_schema(self, schema_name: str, schema_data: Dict[str, Any]) -> Tuple[str, str]:
        """Process enum schema and return enum block and class signature."""
        display_name = schema_name[0].upper() + schema_name[1:]
        enum_block = f'enum "{display_name}" {{\n'
        for value in schema_data['enum']:
            enum_block += f"  {value}\n"
        enum_block += "}\n\n"
        return enum_block, display_name
    
    def _process_class_schema(self, schema_name: str, schema_data: Dict[str, Any]) -> Tuple[str, str, List[str]]:
        """Process class schema and return class block, display name, and relationships."""
        display_name = self._get_display_name(schema_name)
        class_block = f'class "{display_name}" {{\n'
        relationships = []
        
        required_props = schema_data.get("required", [])
        
        if 'properties' in schema_data:
            for prop_name, prop_details in schema_data['properties'].items():
                prop_type = self._get_property_type(prop_details)
                
                # Capitalize non-primitive types
                if prop_type not in ['string', 'object', 'number', 'boolean', 'array']:
                    prop_type = prop_type[0].upper() + prop_type[1:]
                
                suffix = " <<required>>" if prop_name in required_props else ""
                class_block += f"  - {prop_name}: {prop_type}{suffix}\n"
        
        class_block += "}\n\n"
        
        # Generate relationships
        if 'properties' in schema_data:
            for prop_name, prop_details in schema_data['properties'].items():
                prop_type = self._get_property_type(prop_details)
                if prop_type not in ['string', 'object', 'number', 'boolean', 'array']:
                    prop_type = prop_type[0].upper() + prop_type[1:]
                    relationships.append(f"{display_name} --> {prop_type}")
        
        return class_block, display_name, relationships
    
    def _get_display_name(self, schema_name: str) -> str:
        """Get display name for schema, handling special cases."""
        # Only modify display names for domain entities (MovieResponse, RentalResponse, etc.)
        if schema_name in ['MovieResponse', 'RentalResponse', 'UserResponse']:
            # Remove 'Response' suffix for domain entities
            display_name = schema_name.replace('Response', '')
        else:
            # Keep original name for DTOs and other schemas
            display_name = schema_name
        return display_name[0].upper() + display_name[1:]
    
    def _get_property_type(self, prop_details: Dict[str, Any]) -> str:
        """Extract property type from property details."""
        prop_type = prop_details.get('type')
        if not prop_type and '$ref' in prop_details:
            prop_type = prop_details['$ref'].split('/')[-1]
        elif not prop_type:
            prop_type = 'Unknown'
        return prop_type
    
    def _generate_filename(self, service_name: str) -> str:
        """Generate output filename based on service name."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{service_name.lower()}_{timestamp}.puml"
    
    def generate_from_spec(self, spec_data: Dict[str, Any], service_name: str) -> str:
        """
        Generate PlantUML diagram from OpenAPI specification.
        
        Args:
            spec_data: OpenAPI specification data
            service_name: Name of the service
            
        Returns:
            Path to generated PUML file
        """
        relationships = []
        written_classes = set()
        
        # Organize schemas by package
        entity_schemas = []
        dto_schemas = []
        exception_schemas = []
        
        # Start PUML content
        puml_content = self._generate_header(service_name)
        
        # Check if components and schemas exist
        if 'components' not in spec_data or 'schemas' not in spec_data['components']:
            puml_content += "No schemas found in the OpenAPI file.\n"
        else:
            schemas = spec_data['components']['schemas']
            
            # Categorize schemas
            for schema_name, schema_data in schemas.items():
                if 'Error' in schema_name or 'Exception' in schema_name:
                    exception_schemas.append((schema_name, schema_data))
                elif schema_name in ['MovieResponse', 'RentalResponse', 'UserResponse']:
                    # These are domain entities, not DTOs
                    entity_schemas.append((schema_name, schema_data))
                elif 'Request' in schema_name or 'Response' in schema_name:
                    dto_schemas.append((schema_name, schema_data))
                else:
                    # Everything else is an entity (domain models, enums, etc.)
                    entity_schemas.append((schema_name, schema_data))
            
            # Generate entity package
            if entity_schemas:
                puml_content += "\n' Paquete para Entidades de Dominio\n"
                puml_content += 'package "entities" {\n'
                for schema_name, schema_data in entity_schemas:
                    if schema_data.get('type') == 'string' and 'enum' in schema_data:
                        enum_block, display_name = self._process_enum_schema(schema_name, schema_data)
                        puml_content += "    " + enum_block.replace("\n", "\n    ")
                        written_classes.add((display_name,))
                    elif 'properties' in schema_data:
                        class_block, display_name, class_relationships = self._process_class_schema(schema_name, schema_data)
                        puml_content += "    " + class_block.replace("\n", "\n    ")
                        # Update relationships for entity classes
                        for rel in class_relationships:
                            if 'UserStatus' in rel:
                                relationships.append(f"entities.{rel.replace(' --> ', ' --> entities.')}") 
                            else:
                                relationships.append(f"entities.{rel}")
                        written_classes.add((display_name,))
                puml_content += "}\n"
            
            # Generate DTOs package
            if dto_schemas:
                puml_content += "\n' Paquete para DTOs (Data Transfer Objects)\n"
                puml_content += 'package "dtos" {\n'
                for schema_name, schema_data in dto_schemas:
                    if 'properties' in schema_data:
                        class_block, display_name, class_relationships = self._process_class_schema(schema_name, schema_data)
                        puml_content += "    " + class_block.replace("\n", "\n    ")
                        # Update relationships to include package prefixes
                        for rel in class_relationships:
                            if 'UserStatus' in rel:
                                relationships.append(f"dtos.{rel.replace(' --> ', ' --> entities.')}") 
                            else:
                                relationships.append(f"dtos.{rel}")
                        written_classes.add((display_name,))
                puml_content += "}\n"
            
            # Generate Exceptions package
            if exception_schemas:
                puml_content += "\n' Paquete para DTOs de Errores/Excepciones\n"
                puml_content += 'package "Exceptions" {\n'
                for schema_name, schema_data in exception_schemas:
                    if 'properties' in schema_data:
                        class_block, display_name, class_relationships = self._process_class_schema(schema_name, schema_data)
                        puml_content += "    " + class_block.replace("\n", "\n    ")
                        relationships.extend([f"Exceptions.{rel}" for rel in class_relationships])
                        written_classes.add((display_name,))
                puml_content += "}\n"
        
        # Add relationships to PUML content
        if relationships:
            puml_content += "\n\n' Relationships (now crossing package boundaries)\n"
            puml_content += "\n".join(sorted(set(relationships))) + "\n"
        
        puml_content += "\n@enduml\n"
        
        # Generate output path and save
        output_filename = self._generate_filename(service_name)
        output_path = self.output_dir / output_filename
        
        # Ensure directory exists before writing
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as puml_file:
            puml_file.write(puml_content)
        
        print(f"PUML file generated: {output_path}")
        return str(output_path)