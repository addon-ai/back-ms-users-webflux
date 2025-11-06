#!/usr/bin/env python3
"""
Main documentation generator orchestrating architectural diagram generation.
"""

from pathlib import Path
from typing import List, Dict, Any

from .project_analyzer import ProjectAnalyzer
from generators.component_diagram_generator import ComponentDiagramGenerator
from generators.sequence_diagram_generator import SequenceDiagramGenerator


class ArchitectDocsGenerator:
    """Main documentation generator for architectural diagrams."""
    
    def __init__(self, projects_dir: str = "projects", output_dir: str = "docs"):
        self.projects_dir = projects_dir
        self.output_dir = Path(output_dir)
        
        # Initialize components
        self.project_analyzer = ProjectAnalyzer(projects_dir)
        self.component_generator = ComponentDiagramGenerator(
            output_dir=str(self.output_dir / "puml" / "components"),
            templates_dir=str(Path(__file__).parent.parent / "templates")
        )
        self.sequence_generator = SequenceDiagramGenerator(
            templates_dir=str(Path(__file__).parent.parent / "templates")
        )
    
    def clean_docs_directory(self):
        """Clean the diagrams directories before generating new documentation."""
        components_dir = self.output_dir / "puml" / "components"
        sequences_dir = self.output_dir / "puml" / "sequences"
        
        if components_dir.exists():
            import shutil
            shutil.rmtree(components_dir)
            print(f"Cleaned components directory: {components_dir}")
        components_dir.mkdir(parents=True, exist_ok=True)
        
        if sequences_dir.exists():
            import shutil
            shutil.rmtree(sequences_dir)
            print(f"Cleaned sequences directory: {sequences_dir}")
        sequences_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_all_docs(self, clean_first: bool = True) -> Dict[str, List[str]]:
        """
        Generate architectural documentation for all projects.
        
        Args:
            clean_first: Whether to clean the docs directory before generating
            
        Returns:
            Dictionary mapping format names to lists of generated file paths
        """
        if clean_first:
            self.clean_docs_directory()
        
        # Discover and analyze projects
        projects = self.project_analyzer.discover_projects()
        if not projects:
            print("No Java projects found in projects directory")
            return {"component_diagrams": []}
        
        print(f"Found {len(projects)} projects: {[p['name'] for p in projects]}")
        
        # Generate diagrams
        generated_files = {"component_diagrams": [], "sequence_diagrams": []}
        
        for project in projects:
            print(f"\nGenerating diagrams for {project['name']}...")
            
            # Generate component diagram
            try:
                diagram_path = self.component_generator.generate_component_diagram(project)
                generated_files["component_diagrams"].append(diagram_path)
                print(f"  ✓ Component diagram: {diagram_path}")
            except Exception as e:
                print(f"  ✗ Error generating component diagram: {e}")
            
            # Generate sequence diagrams
            try:
                sequence_paths = self.sequence_generator.generate_sequence_diagrams(project, str(self.output_dir))
                generated_files["sequence_diagrams"].extend(sequence_paths)
                print(f"  ✓ Generated {len(sequence_paths)} sequence diagrams")
            except Exception as e:
                print(f"  ✗ Error generating sequence diagrams: {e}")
        
        return generated_files
    
    def generate_for_project(self, project_name: str) -> Dict[str, str]:
        """
        Generate documentation for a specific project.
        
        Args:
            project_name: Name of the project to generate docs for
            
        Returns:
            Dictionary mapping format names to generated file paths
        """
        projects = self.project_analyzer.discover_projects()
        project = next((p for p in projects if p['name'] == project_name), None)
        
        if not project:
            print(f"Project '{project_name}' not found")
            return {}
        
        generated_files = {}
        
        print(f"Generating diagrams for {project_name}...")
        
        # Generate component diagram
        try:
            generated_files['component_diagram'] = self.component_generator.generate_component_diagram(project)
            print(f"  ✓ Component diagram generated")
        except Exception as e:
            print(f"  ✗ Error generating component diagram: {e}")
        
        # Generate sequence diagrams
        try:
            sequence_paths = self.sequence_generator.generate_sequence_diagrams(project, str(self.output_dir))
            generated_files['sequence_diagrams'] = sequence_paths
            print(f"  ✓ Generated {len(sequence_paths)} sequence diagrams")
        except Exception as e:
            print(f"  ✗ Error generating sequence diagrams: {e}")
        
        return generated_files
    
    def list_projects(self) -> List[str]:
        """List all discovered projects."""
        projects = self.project_analyzer.discover_projects()
        return [project['name'] for project in projects]