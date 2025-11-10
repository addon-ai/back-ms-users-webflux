#!/usr/bin/env python3
"""
Backstage Golden Path Generator
Converts generated Java projects into Backstage Software Templates (Golden Paths)
"""
import os
import re
import shutil
import json
from pathlib import Path
import pystache


class BackstageGoldenPathGenerator:
    """Generates Backstage Golden Paths from Java projects."""
    
    def __init__(self, config_path: str):
        """Initialize with configuration."""
        with open(config_path, 'r') as f:
            self.projects = json.load(f)
        self.templates_dir = Path(__file__).parent / 'templates'
    
    def generate_all(self, projects_dir: str, output_dir: str):
        """Generate Golden Paths for all projects."""
        projects_path = Path(projects_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        for project_config in self.projects:
            project_name = project_config['project']['general']['name']
            source_project = projects_path / project_name
            
            if not source_project.exists():
                print(f"⚠️  Project {project_name} not found, skipping...")
                continue
            
            # Determine stack type
            stack_type = 'webflux' if 'webflux' in project_name.lower() else 'springboot'
            template_name = f"{stack_type}-service"
            
            print(f"📦 Generating Golden Path for {project_name} ({stack_type})...")
            self.generate_golden_path(source_project, output_path / template_name, project_config, stack_type)
    
    def generate_golden_path(self, source_project: Path, output_path: Path, project_config: dict, stack_type: str):
        """Generate a single Golden Path."""
        # 1. Create skeleton directory
        skeleton_path = output_path / 'skeleton'
        if skeleton_path.exists():
            shutil.rmtree(skeleton_path)
        shutil.copytree(source_project, skeleton_path)
        
        # 2. Re-parametrize skeleton
        project_info = project_config['project']
        hardcoded_name = project_info['general']['name']
        hardcoded_group = project_info['params']['basePackage']
        
        self._reparametrize_skeleton(skeleton_path, hardcoded_name, hardcoded_group)
        
        # 3. Generate template.yaml
        template_vars = {
            'template_id': f"{stack_type}-service-template",
            'template_title': f"Java {stack_type.title()} Service",
            'template_description': f"Create a new Java {stack_type.title()} microservice with hexagonal architecture",
            'stack_type': stack_type,
            'default_owner': 'platform-team',
            'default_groupId': 'com.example',
            'default_javaVersion': project_config.get('devops', {}).get('ci', {}).get('javaVersion', '21')
        }
        
        self._render_template('template.yaml.mustache', output_path / 'template.yaml', template_vars)
        
        # 4. Generate catalog-info.yaml for skeleton
        catalog_vars = {
            'system_name': 'backend-services'
        }
        
        self._render_template('catalog-info.yaml.mustache', skeleton_path / 'catalog-info.yaml', catalog_vars)
        
        print(f"✅ Golden Path created at {output_path}")
    
    def _reparametrize_skeleton(self, skeleton_path: Path, hardcoded_name: str, hardcoded_group: str):
        """Replace hardcoded values with Backstage template variables."""
        # Patterns to replace
        replacements = {
            # Maven/Gradle artifacts
            f'<artifactId>{hardcoded_name}</artifactId>': '<artifactId>${{ values.component_id }}</artifactId>',
            f'<groupId>{hardcoded_group}</groupId>': '<groupId>${{ values.groupId }}</groupId>',
            f'<name>{hardcoded_name}</name>': '<name>${{ values.component_id }}</name>',
            
            # Application properties
            f'spring.application.name={hardcoded_name}': 'spring.application.name=${{ values.component_id }}',
            
            # Java packages
            f'package {hardcoded_group}': 'package ${{ values.java_package_name }}',
            f'import {hardcoded_group}': 'import ${{ values.java_package_name }}',
        }
        
        # Process all text files
        for root, dirs, files in os.walk(skeleton_path):
            # Skip .git and target directories
            dirs[:] = [d for d in dirs if d not in ['.git', 'target', 'node_modules', '.idea']]
            
            for file in files:
                if file.endswith(('.java', '.xml', '.properties', '.yml', '.yaml', '.md')):
                    file_path = Path(root) / file
                    try:
                        content = file_path.read_text(encoding='utf-8')
                        
                        # Apply replacements
                        for old, new in replacements.items():
                            content = content.replace(old, new)
                        
                        file_path.write_text(content, encoding='utf-8')
                    except Exception as e:
                        print(f"⚠️  Could not process {file_path}: {e}")
        
        # Rename package directories
        self._rename_package_dirs(skeleton_path, hardcoded_group)
    
    def _rename_package_dirs(self, skeleton_path: Path, hardcoded_group: str):
        """Rename Java package directories to template variables."""
        src_main_java = skeleton_path / 'src' / 'main' / 'java'
        src_test_java = skeleton_path / 'src' / 'test' / 'java'
        
        for base_path in [src_main_java, src_test_java]:
            if not base_path.exists():
                continue
            
            # Find the package root (e.g., com/example/userservice)
            package_path = base_path / hardcoded_group.replace('.', '/')
            if package_path.exists():
                # Create placeholder directory structure
                placeholder_path = base_path / '${{ values.java_package_path }}'
                placeholder_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Move contents
                if placeholder_path.exists():
                    shutil.rmtree(placeholder_path)
                shutil.move(str(package_path), str(placeholder_path))
                
                # Clean up old package structure
                old_root = base_path / hardcoded_group.split('.')[0]
                if old_root.exists() and old_root != placeholder_path:
                    try:
                        shutil.rmtree(old_root)
                    except:
                        pass
    
    def _render_template(self, template_name: str, output_path: Path, context: dict):
        """Render a Mustache template."""
        template_path = self.templates_dir / template_name
        template_content = template_path.read_text(encoding='utf-8')
        rendered = pystache.render(template_content, context)
        output_path.write_text(rendered, encoding='utf-8')


def main():
    """Main entry point."""
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: python main.py <config_path> <projects_dir> <output_dir>")
        sys.exit(1)
    
    config_path = sys.argv[1]
    projects_dir = sys.argv[2]
    output_dir = sys.argv[3]
    
    generator = BackstageGoldenPathGenerator(config_path)
    generator.generate_all(projects_dir, output_dir)
    
    print("\n✅ All Golden Paths generated successfully!")


if __name__ == '__main__':
    main()
