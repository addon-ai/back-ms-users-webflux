#!/usr/bin/env python3
"""
Project analyzer for extracting architectural information from generated Java projects.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
import ast


class ProjectAnalyzer:
    """Analyzes Java project structure to extract architectural components."""
    
    def __init__(self, projects_dir: str = "projects"):
        self.projects_dir = Path(projects_dir)
    
    def discover_projects(self) -> List[Dict[str, Any]]:
        """Discover all Java projects in the projects directory."""
        projects = []
        
        if not self.projects_dir.exists():
            return projects
            
        for project_path in self.projects_dir.iterdir():
            if project_path.is_dir() and self._is_java_project(project_path):
                project_info = self._analyze_project(project_path)
                if project_info:
                    projects.append(project_info)
        
        return projects
    
    def _is_java_project(self, project_path: Path) -> bool:
        """Check if directory is a Java project."""
        return (project_path / "pom.xml").exists() and (project_path / "src").exists()
    
    def _analyze_project(self, project_path: Path) -> Optional[Dict[str, Any]]:
        """Analyze a single Java project."""
        project_name = project_path.name
        src_path = project_path / "src" / "main" / "java"
        
        if not src_path.exists():
            return None
        
        # Find base package
        base_package_path = self._find_base_package(src_path)
        if not base_package_path:
            return None
        
        return {
            "name": project_name,
            "path": str(project_path),
            "base_package": self._path_to_package(base_package_path, src_path),
            "layers": self._analyze_layers(base_package_path),
            "entities": self._extract_entities(base_package_path),
            "controllers": self._extract_controllers(base_package_path),
            "services": self._extract_services(base_package_path),
            "repositories": self._extract_repositories(base_package_path),
            "exceptions": self._extract_exceptions(base_package_path)
        }
    
    def _find_base_package(self, src_path: Path) -> Optional[Path]:
        """Find the base package directory."""
        for root, dirs, files in os.walk(src_path):
            root_path = Path(root)
            if any(d in ["domain", "application", "infrastructure"] for d in dirs):
                return root_path
        return None
    
    def _path_to_package(self, package_path: Path, src_path: Path) -> str:
        """Convert file path to Java package name."""
        relative_path = package_path.relative_to(src_path)
        return str(relative_path).replace(os.sep, ".")
    
    def _analyze_layers(self, base_path: Path) -> Dict[str, Any]:
        """Analyze hexagonal architecture layers."""
        layers = {
            "domain": {"models": [], "ports": {"input": [], "output": []}},
            "application": {"services": [], "mappers": [], "dtos": []},
            "infrastructure": {"controllers": [], "adapters": [], "persistence": [], "config": [], "exceptions": []}
        }
        
        # Domain layer
        domain_path = base_path / "domain"
        if domain_path.exists():
            layers["domain"]["models"] = self._extract_java_classes(domain_path / "model")
            layers["domain"]["ports"]["input"] = self._extract_java_classes(domain_path / "ports" / "input")
            layers["domain"]["ports"]["output"] = self._extract_java_classes(domain_path / "ports" / "output")
        
        # Application layer
        app_path = base_path / "application"
        if app_path.exists():
            layers["application"]["services"] = self._extract_java_classes(app_path / "service")
            layers["application"]["mappers"] = self._extract_java_classes(app_path / "mapper")
            layers["application"]["dtos"] = self._extract_java_classes(app_path / "dto", recursive=True)
        
        # Infrastructure layer
        infra_path = base_path / "infrastructure"
        if infra_path.exists():
            layers["infrastructure"]["controllers"] = self._extract_java_classes(infra_path / "adapters" / "input" / "rest")
            layers["infrastructure"]["adapters"] = self._extract_java_classes(infra_path / "adapters" / "output" / "persistence" / "adapter")
            layers["infrastructure"]["persistence"] = {
                "repositories": self._extract_java_classes(infra_path / "adapters" / "output" / "persistence" / "repository"),
                "entities": self._extract_java_classes(infra_path / "adapters" / "output" / "persistence" / "entity")
            }
            # Extract config classes from both config/ and root level
            config_classes = self._extract_java_classes(infra_path / "config")
            # Also check for ApplicationConfiguration at root level
            root_config = self._extract_java_classes(base_path.parent, pattern="*Configuration.java")
            layers["infrastructure"]["config"] = config_classes + root_config
            layers["infrastructure"]["exceptions"] = self._extract_java_classes(infra_path / "config" / "exceptions")
        
        return layers
    
    def _extract_java_classes(self, path: Path, recursive: bool = False, pattern: str = "*.java") -> List[Dict[str, Any]]:
        """Extract Java class information from a directory."""
        classes = []
        
        if not path.exists():
            return classes
        
        search_pattern = "**/*.java" if recursive else pattern
        for java_file in path.glob(search_pattern):
            class_info = self._parse_java_file(java_file)
            if class_info:
                classes.append(class_info)
        
        return classes
    
    def _parse_java_file(self, java_file: Path) -> Optional[Dict[str, Any]]:
        """Parse a Java file to extract class information."""
        try:
            with open(java_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract class name - improved regex
            class_patterns = [
                r'public\s+(?:final\s+)?(?:class|interface|enum)\s+(\w+)',
                r'(?:class|interface|enum)\s+(\w+)',
                r'@\w+\s*\n\s*public\s+(?:class|interface|enum)\s+(\w+)'
            ]
            
            class_name = None
            for pattern in class_patterns:
                class_match = re.search(pattern, content, re.MULTILINE)
                if class_match:
                    class_name = class_match.group(1)
                    break
            
            if not class_name:
                # Fallback: use filename without extension
                class_name = java_file.stem
            
            # Extract annotations
            annotations = re.findall(r'@(\w+)', content)
            
            # Extract methods
            methods = self._extract_methods(content)
            
            # Extract fields
            fields = self._extract_fields(content)
            
            return {
                "name": class_name,
                "file": str(java_file),
                "annotations": annotations,
                "methods": methods,
                "fields": fields,
                "type": self._determine_class_type(content, annotations)
            }
        
        except Exception as e:
            print(f"Error parsing {java_file}: {e}")
            return None
    
    def _extract_methods(self, content: str) -> List[Dict[str, str]]:
        """Extract method signatures from Java content."""
        methods = []
        
        # Pattern specifically for REST controller methods
        controller_patterns = [
            r'public\s+ResponseEntity<\w+>\s+(\w+)\s*\(',  # public ResponseEntity<Type> methodName(
            r'public\s+(?:\w+(?:<[^>]+>)?)\s+(\w+)\s*\(',   # public Type methodName(
            r'@\w+Mapping[^\n]*\n\s*public\s+(?:\w+(?:<[^>]+>)?)\s+(\w+)\s*\('  # @GetMapping etc.
        ]
        
        for pattern in controller_patterns:
            for match in re.finditer(pattern, content, re.MULTILINE):
                method_name = match.group(1)
                if method_name not in ['class', 'interface', 'enum', 'if', 'for', 'while', 'switch']:
                    methods.append({
                        "name": method_name,
                        "signature": match.group(0).strip()
                    })
        
        # Remove duplicates
        seen = set()
        unique_methods = []
        for method in methods:
            if method["name"] not in seen:
                seen.add(method["name"])
                unique_methods.append(method)
        
        return unique_methods
    
    def _extract_fields(self, content: str) -> List[Dict[str, str]]:
        """Extract field declarations from Java content."""
        fields = []
        # Simplified field extraction
        field_pattern = r'(?:private|protected|public)?\s+(?:static\s+)?(?:final\s+)?(\w+(?:<[^>]+>)?)\s+(\w+)\s*[;=]'
        
        for match in re.finditer(field_pattern, content):
            field_type = match.group(1)
            field_name = match.group(2)
            fields.append({
                "name": field_name,
                "type": field_type
            })
        
        return fields
    
    def _determine_class_type(self, content: str, annotations: List[str]) -> str:
        """Determine the type of class based on content and annotations."""
        if 'interface' in content:
            return 'interface'
        elif 'enum' in content:
            return 'enum'
        elif any(ann in annotations for ann in ['RestController', 'Controller']):
            return 'controller'
        elif any(ann in annotations for ann in ['Service', 'Component']):
            return 'service'
        elif any(ann in annotations for ann in ['Repository']):
            return 'repository'
        elif any(ann in annotations for ann in ['Entity', 'Table']):
            return 'entity'
        elif any(ann in annotations for ann in ['Mapper']):
            return 'mapper'
        elif 'Exception' in content:
            return 'exception'
        else:
            return 'class'
    
    def _extract_entities(self, base_path: Path) -> List[str]:
        """Extract domain entity names."""
        entities = []
        domain_models_path = base_path / "domain" / "model"
        
        if domain_models_path.exists():
            for java_file in domain_models_path.glob("*.java"):
                class_info = self._parse_java_file(java_file)
                if class_info and class_info["name"] != "EntityStatus":
                    entities.append(class_info["name"])
        
        return entities
    
    def _extract_controllers(self, base_path: Path) -> List[str]:
        """Extract controller names."""
        controllers = []
        controllers_path = base_path / "infrastructure" / "adapters" / "input" / "rest"
        
        if controllers_path.exists():
            for java_file in controllers_path.glob("*.java"):
                class_info = self._parse_java_file(java_file)
                if class_info:
                    controllers.append(class_info["name"])
        
        return controllers
    
    def _extract_services(self, base_path: Path) -> List[str]:
        """Extract service names."""
        services = []
        services_path = base_path / "application" / "service"
        
        if services_path.exists():
            for java_file in services_path.glob("*.java"):
                class_info = self._parse_java_file(java_file)
                if class_info:
                    services.append(class_info["name"])
        
        return services
    
    def _extract_repositories(self, base_path: Path) -> List[str]:
        """Extract repository names."""
        repositories = []
        repo_path = base_path / "infrastructure" / "adapters" / "output" / "persistence"
        
        for subdir in ["repository", "adapter"]:
            subdir_path = repo_path / subdir
            if subdir_path.exists():
                for java_file in subdir_path.glob("*.java"):
                    class_info = self._parse_java_file(java_file)
                    if class_info:
                        repositories.append(class_info["name"])
        
        return repositories
    
    def _extract_exceptions(self, base_path: Path) -> List[str]:
        """Extract custom exception names."""
        exceptions = []
        exceptions_path = base_path / "infrastructure" / "config" / "exceptions"
        
        if exceptions_path.exists():
            for java_file in exceptions_path.glob("*.java"):
                class_info = self._parse_java_file(java_file)
                if class_info and "Exception" in class_info["name"]:
                    exceptions.append(class_info["name"])
        
        return exceptions