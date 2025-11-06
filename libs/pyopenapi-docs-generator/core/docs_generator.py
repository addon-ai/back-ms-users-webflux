#!/usr/bin/env python3
"""
Main documentation generator orchestrating all output formats.
"""

from pathlib import Path
from typing import Dict, Any, List
import shutil

from .openapi_processor import OpenApiProcessor
from generators.puml_generator import PumlGenerator
from generators.markdown_generator import MarkdownGenerator
from generators.txt_generator import TxtGenerator


class DocsGenerator:
    """Main documentation generator for OpenAPI specifications."""
    
    def __init__(self, build_dir: str = "build/smithy", output_dir: str = "docs"):
        """
        Initialize the documentation generator.
        
        Args:
            build_dir: Directory containing Smithy build outputs
            output_dir: Base directory for generated documentation
        """
        self.openapi_processor = OpenApiProcessor(build_dir)
        self.output_dir = Path(output_dir)
        
        # Ensure base output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize generators with absolute paths
        self.puml_generator = PumlGenerator(str(self.output_dir / "puml" / "open-api"))
        self.markdown_generator = MarkdownGenerator(str(self.output_dir / "md"))
        self.txt_generator = TxtGenerator(str(self.output_dir / "txt"))
    
    def clean_docs_directory(self):
        """Clean the docs directory before generating new documentation."""
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
            print(f"Cleaned docs directory: {self.output_dir}")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_all_docs(self, formats: List[str] = None, clean_first: bool = True) -> Dict[str, List[str]]:
        """
        Generate documentation in all specified formats for all OpenAPI specs.
        
        Args:
            formats: List of formats to generate ('puml', 'md', 'txt').
                    If None, generates all formats.
            clean_first: Whether to clean the docs directory before generating
        
        Returns:
            Dictionary mapping format names to lists of generated file paths
        """
        if formats is None:
            formats = ['puml', 'md', 'txt']
        
        # Clean docs directory if requested
        if clean_first:
            self.clean_docs_directory()
        
        # Load all OpenAPI specifications
        specs = self.openapi_processor.load_openapi_specs()
        if not specs:
            print("No OpenAPI specifications found in build directory")
            return {}
        
        generated_files = {format_name: [] for format_name in formats}
        
        # Generate documentation for each spec
        for spec_info in specs:
            service_name = spec_info['service_name']
            spec_data = spec_info['spec']
            
            print(f"\nGenerating documentation for {service_name}...")
            
            if 'puml' in formats:
                try:
                    puml_path = self.puml_generator.generate_from_spec(spec_data, service_name)
                    generated_files['puml'].append(puml_path)
                except Exception as e:
                    print(f"Error generating PUML for {service_name}: {e}")
            
            if 'md' in formats:
                try:
                    md_path = self.markdown_generator.generate_from_spec(spec_data, service_name)
                    generated_files['md'].append(md_path)
                except Exception as e:
                    print(f"Error generating Markdown for {service_name}: {e}")
            

            
            if 'txt' in formats:
                try:
                    txt_path = self.txt_generator.generate_from_spec(spec_data, service_name)
                    generated_files['txt'].append(txt_path)
                except Exception as e:
                    print(f"Error generating TXT for {service_name}: {e}")
        
        return generated_files
    
    def generate_for_service(self, service_name: str, formats: List[str] = None) -> Dict[str, str]:
        """
        Generate documentation for a specific service.
        
        Args:
            service_name: Name of the service to generate docs for
            formats: List of formats to generate
        
        Returns:
            Dictionary mapping format names to generated file paths
        """
        if formats is None:
            formats = ['puml', 'md', 'txt']
        
        spec_info = self.openapi_processor.get_spec_by_service(service_name)
        if not spec_info:
            print(f"Service '{service_name}' not found")
            return {}
        
        spec_data = spec_info['spec']
        generated_files = {}
        
        print(f"Generating documentation for {service_name}...")
        
        if 'puml' in formats:
            try:
                generated_files['puml'] = self.puml_generator.generate_from_spec(spec_data, service_name)
            except Exception as e:
                print(f"Error generating PUML: {e}")
        
        if 'md' in formats:
            try:
                generated_files['md'] = self.markdown_generator.generate_from_spec(spec_data, service_name)
            except Exception as e:
                print(f"Error generating Markdown: {e}")
        

        
        if 'txt' in formats:
            try:
                generated_files['txt'] = self.txt_generator.generate_from_spec(spec_data, service_name)
            except Exception as e:
                print(f"Error generating TXT: {e}")
        
        return generated_files