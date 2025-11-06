#!/usr/bin/env python3
"""
Component diagram generator for hexagonal architecture projects.
"""

import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
import pystache


class ComponentDiagramGenerator:
    """Generates PlantUML component diagrams from project analysis."""
    
    def __init__(self, output_dir: str = "docs/puml/components", templates_dir: str = None):
        self.output_dir = Path(output_dir)
        self.templates_dir = Path(templates_dir) if templates_dir else Path(__file__).parent.parent / "templates"
        self._ensure_output_directory()
    
    def _ensure_output_directory(self) -> None:
        """Ensure the output directory exists."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_component_diagram(self, project_info: Dict[str, Any]) -> str:
        """Generate a component diagram for a project."""
        template_path = self.templates_dir / "component_diagram.mustache"
        
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        # Prepare template context
        context = self._prepare_template_context(project_info)
        
        # Load and render template
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        
        rendered_content = pystache.render(template, context)
        
        # Generate output filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f"{project_info['name']}_{timestamp}.puml"
        output_path = self.output_dir / output_filename
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(rendered_content)
        
        print(f"Component diagram generated: {output_path}")
        return str(output_path)
    
    def _prepare_template_context(self, project_info: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare context data for template rendering."""
        layers = project_info.get("layers", {})
        
        # Extract components by layer
        domain_models = layers.get("domain", {}).get("models", [])
        input_ports = layers.get("domain", {}).get("ports", {}).get("input", [])
        output_ports = layers.get("domain", {}).get("ports", {}).get("output", [])
        
        services = layers.get("application", {}).get("services", [])
        mappers = layers.get("application", {}).get("mappers", [])
        dtos = layers.get("application", {}).get("dtos", [])
        
        controllers = layers.get("infrastructure", {}).get("controllers", [])
        adapters = layers.get("infrastructure", {}).get("adapters", [])
        persistence = layers.get("infrastructure", {}).get("persistence", {})
        config = layers.get("infrastructure", {}).get("config", [])
        exceptions = layers.get("infrastructure", {}).get("exceptions", [])
        
        # Group DTOs by entity
        dto_groups = self._group_dtos(dtos)
        
        # Create JPA repository to DBO mappings
        jpa_dbo_mappings = self._create_jpa_dbo_mappings(
            persistence.get("repositories", []),
            persistence.get("entities", [])
        )
        
        context = {
            "project_name": project_info["name"],
            "project_title": self._format_title(project_info["name"]),
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            
            # Domain layer
            "domain_models": [{"name": cls["name"]} for cls in domain_models],
            "input_ports": [{"name": cls["name"]} for cls in input_ports],
            "output_ports": [{"name": cls["name"]} for cls in output_ports],
            
            # Application layer
            "services": [{"name": cls["name"]} for cls in services],
            "mappers": [{"name": cls["name"]} for cls in mappers],
            "dto_groups": dto_groups,
            "has_logging_utils": any("LoggingUtils" in cls["name"] for cls in layers.get("application", {}).get("services", [])),
            
            # Infrastructure layer
            "controllers": [{"name": cls["name"]} for cls in controllers],
            "adapters": [{"name": cls["name"]} for cls in adapters],
            "jpa_repositories": [{"name": cls["name"]} for cls in persistence.get("repositories", [])],
            "jpa_entities": [{"name": cls["name"]} for cls in persistence.get("entities", [])],
            "jpa_dbo_mappings": jpa_dbo_mappings,
            "config_classes": [{"name": cls["name"]} for cls in config],
            "exceptions": [{"name": cls["name"]} for cls in exceptions],
            
            # Statistics
            "entity_count": len(domain_models),
            "use_case_count": len(input_ports),
            "repository_count": len(output_ports),
            "service_count": len(services),
            "mapper_count": len(mappers),
            "exception_count": len(exceptions),
            
            # Flags for conditional rendering
            "has_domain_models": len(domain_models) > 0,
            "has_input_ports": len(input_ports) > 0,
            "has_output_ports": len(output_ports) > 0,
            "has_services": len(services) > 0,
            "has_mappers": len(mappers) > 0,
            "has_dtos": len(dtos) > 0,
            "has_controllers": len(controllers) > 0,
            "has_adapters": len(adapters) > 0,
            "has_jpa_repositories": len(persistence.get("repositories", [])) > 0,
            "has_jpa_entities": len(persistence.get("entities", [])) > 0,
            "has_config": len(config) > 0,
            "has_exceptions": len(exceptions) > 0
        }
        
        return context
    
    def _group_dtos(self, dtos: list) -> list:
        """Group DTOs by entity type."""
        groups = {}
        
        for dto in dtos:
            dto_name = dto["name"]
            
            # Extract entity name from DTO name
            entity_name = self._extract_entity_from_dto(dto_name)
            
            if entity_name not in groups:
                groups[entity_name] = {
                    "entity_name": entity_name,
                    "dtos": []
                }
            
            groups[entity_name]["dtos"].append({"name": dto_name})
        
        return list(groups.values())
    
    def _extract_entity_from_dto(self, dto_name: str) -> str:
        """Extract entity name from DTO class name."""
        # Remove common DTO suffixes
        for suffix in ["RequestContent", "ResponseContent", "Request", "Response", "DTO"]:
            if dto_name.endswith(suffix):
                dto_name = dto_name[:-len(suffix)]
        
        # Remove common prefixes
        for prefix in ["Create", "Update", "Delete", "Get", "List"]:
            if dto_name.startswith(prefix):
                dto_name = dto_name[len(prefix):]
        
        # Handle special cases
        if dto_name.endswith("s"):  # ListUsers -> User
            dto_name = dto_name[:-1]
        
        return dto_name if dto_name else "Unknown"
    
    def _format_title(self, project_name: str) -> str:
        """Format project name for display."""
        return project_name.replace("-", " ").replace("_", " ").title()
    
    def _create_jpa_dbo_mappings(self, repositories: list, entities: list) -> list:
        """Create mappings between JPA repositories and DBO entities."""
        mappings = []
        
        for repo in repositories:
            repo_name = repo["name"]
            # Extract entity name from repository name
            # JpaMovieRepository -> Movie
            if repo_name.startswith("Jpa") and repo_name.endswith("Repository"):
                entity_name = repo_name[3:-10]  # Remove "Jpa" and "Repository"
                dbo_name = f"{entity_name}Dbo"
                
                # Check if corresponding DBO exists
                if any(entity["name"] == dbo_name for entity in entities):
                    mappings.append({
                        "jpa_repo": repo_name,
                        "dbo_entity": dbo_name
                    })
        
        return mappings
    
    def generate_all_diagrams(self, projects: list) -> list:
        """Generate component diagrams for all projects."""
        generated_files = []
        
        for project_info in projects:
            try:
                output_path = self.generate_component_diagram(project_info)
                generated_files.append(output_path)
            except Exception as e:
                print(f"Error generating diagram for {project_info['name']}: {e}")
        
        return generated_files