#!/usr/bin/env python3
"""
Main entry point for architectural documentation generation.
"""

import argparse
import sys
from pathlib import Path

from core.docs_generator import ArchitectDocsGenerator


def main():
    """Main entry point for the architectural documentation generator."""
    parser = argparse.ArgumentParser(
        description="Generate architectural diagrams from Java projects"
    )
    
    parser.add_argument(
        "--projects-dir",
        default="projects",
        help="Directory containing Java projects (default: projects)"
    )
    
    parser.add_argument(
        "--output-dir", 
        default="docs",
        help="Base directory for generated documentation (default: docs)"
    )
    
    parser.add_argument(
        "--project",
        help="Generate documentation for specific project only"
    )
    
    parser.add_argument(
        "--list-projects",
        action="store_true",
        help="List all discovered projects and exit"
    )
    
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Don't clean output directory before generating"
    )
    
    args = parser.parse_args()
    
    # Validate projects directory exists
    projects_path = Path(args.projects_dir)
    if not projects_path.exists():
        print(f"Error: Projects directory not found: {projects_path}")
        sys.exit(1)
    
    # Initialize generator
    generator = ArchitectDocsGenerator(args.projects_dir, args.output_dir)
    
    try:
        if args.list_projects:
            # List projects and exit
            projects = generator.list_projects()
            if projects:
                print("Discovered projects:")
                for project in projects:
                    print(f"  - {project}")
            else:
                print("No Java projects found")
            return
        
        if args.project:
            # Generate for specific project
            generated_files = generator.generate_for_project(args.project)
            if generated_files:
                print(f"\nDocumentation generated for {args.project}:")
                for format_name, file_path in generated_files.items():
                    print(f"  {format_name.upper()}: {file_path}")
            else:
                print(f"No documentation generated for project: {args.project}")
        else:
            # Generate for all projects
            generated_files = generator.generate_all_docs(clean_first=not args.no_clean)
            
            print("\nArchitectural documentation generation complete!")
            for format_name, file_paths in generated_files.items():
                if file_paths:
                    print(f"\n{format_name.upper().replace('_', ' ')} files generated:")
                    for file_path in file_paths:
                        print(f"  - {file_path}")
    
    except Exception as e:
        print(f"Error during documentation generation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()