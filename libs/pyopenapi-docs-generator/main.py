#!/usr/bin/env python3
"""
Main entry point for OpenAPI documentation generation.
"""

import argparse
import sys
from pathlib import Path

from core.docs_generator import DocsGenerator


def main():
    """Main entry point for the documentation generator."""
    parser = argparse.ArgumentParser(
        description="Generate documentation from OpenAPI specifications"
    )
    
    parser.add_argument(
        "--build-dir",
        default="schemas",
        help="Directory containing schema outputs (default: schemas)"
    )
    
    parser.add_argument(
        "--output-dir", 
        default="docs",
        help="Base directory for generated documentation (default: docs)"
    )
    
    parser.add_argument(
        "--formats",
        nargs="+",
        choices=["puml", "md", "pdf", "txt"],
        default=["puml", "md", "pdf", "txt"],
        help="Documentation formats to generate (default: all)"
    )
    
    parser.add_argument(
        "--service",
        help="Generate documentation for specific service only"
    )
    
    args = parser.parse_args()
    
    # Validate build directory exists
    build_path = Path(args.build_dir)
    if not build_path.exists():
        print(f"Error: Build directory not found: {build_path}")
        sys.exit(1)
    
    # Initialize generator (output_dir is ignored, uses fixed docs/ paths)
    generator = DocsGenerator(args.build_dir, args.output_dir)
    
    try:
        if args.service:
            # Generate for specific service
            generated_files = generator.generate_for_service(args.service, args.formats)
            if generated_files:
                print(f"\nDocumentation generated for {args.service}:")
                for format_name, file_path in generated_files.items():
                    print(f"  {format_name.upper()}: {file_path}")
            else:
                print(f"No documentation generated for service: {args.service}")
        else:
            # Generate for all services
            generated_files = generator.generate_all_docs(args.formats)
            
            print("\nDocumentation generation complete!")
            for format_name, file_paths in generated_files.items():
                if file_paths:
                    print(f"\n{format_name.upper()} files generated:")
                    for file_path in file_paths:
                        print(f"  - {file_path}")
    
    except Exception as e:
        print(f"Error during documentation generation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()