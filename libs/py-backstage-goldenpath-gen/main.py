#!/usr/bin/env python3
"""
Backstage Golden Path Generator
Generates Backstage Software Templates from Java projects
"""
import os
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
        """Generate Backstage templates for all projects."""
        projects_path = Path(projects_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        template_info = []
        
        for project_config in self.projects:
            project_name = project_config['project']['general']['name']
            source_project = projects_path / project_name
            
            if not source_project.exists():
                print(f"⚠️  Project {project_name} not found, skipping...")
                continue
            
            project_type = project_config['project']['general']['type']
            stack_type = 'webflux' if project_type == 'springWebflux' else 'springboot'
            
            print(f"📦 Generating Backstage template for {project_name} ({stack_type})...")
            template_data = self.generate_template(source_project, output_path / project_name, project_config, stack_type)
            template_info.append(template_data)
        
        if template_info:
            self._generate_root_catalog(output_path, template_info)
            self._generate_type_docs(output_path)
    
    def generate_template(self, source_project: Path, output_path: Path, project_config: dict, stack_type: str):
        """Generate a single Backstage template with skeleton."""
        skeleton_path = output_path / 'skeleton'
        if skeleton_path.exists():
            shutil.rmtree(skeleton_path)
        
        def ignore_files(dir, files):
            return [f for f in files if f.endswith(('.java', '.sql')) or f in ('devops', 'target', '.git')]
        
        shutil.copytree(source_project, skeleton_path, ignore=ignore_files)
        
        project_info = project_config['project']
        project_name = project_info['general']['name']
        github_org = project_config.get('devops', {}).get('github', {}).get('organization', 'your-org')
        
        # Generate template.yaml
        template_vars = {
            'template_id': f"{project_name}-template",
            'template_title': project_info['general']['description'],
            'template_description': project_info['general']['description'],
            'stack_type': stack_type,
            'default_owner': 'platform-team',
            'default_groupId': project_info['params']['groupId'],
            'default_artifactId': project_info['params']['artifactId'],
            'default_javaVersion': project_config.get('devops', {}).get('ci', {}).get('javaVersion', '21'),
            'default_springBootVersion': project_info['dependencies'].get('springBoot', '3.2.5'),
            'default_coverageThreshold': project_config.get('devops', {}).get('ci', {}).get('coverageThreshold', '85'),
            'github_org': github_org
        }
        
        self._render_template('template.yaml.mustache', output_path / 'template.yaml', template_vars)
        
        # Generate catalog-info.yaml at template level
        self._render_template('template-catalog-info.yaml.mustache', output_path / 'catalog-info.yaml', template_vars)
        
        # Generate catalog-info.yaml for skeleton
        catalog_vars = {
            'system_name': 'backend-services',
            'stack_type': stack_type,
            'is_webflux': stack_type == 'webflux'
        }
        
        self._render_template('catalog-info.yaml.mustache', skeleton_path / 'catalog-info.yaml', catalog_vars)
        
        print(f"✅ Backstage template created at {output_path}")
        
        return {
            'template_id': template_vars['template_id'],
            'template_title': template_vars['template_title'],
            'template_folder': output_path.name
        }
    
    def _render_template(self, template_name: str, output_path: Path, context: dict):
        """Render a Mustache template."""
        template_path = self.templates_dir / template_name
        template_content = template_path.read_text(encoding='utf-8')
        rendered = pystache.render(template_content, context)
        output_path.write_text(rendered, encoding='utf-8')
    
    def _generate_root_catalog(self, output_path: Path, template_info: list):
        """Generate root catalog-info.yaml."""
        github_org = self.projects[0].get('devops', {}).get('github', {}).get('organization', 'your-org')
        
        catalog_content = [
            "apiVersion: backstage.io/v1alpha1",
            "kind: Component",
            "metadata:",
            "  name: hexagonal-architecture-templates",
            "  description: |",
            "    Spring Boot service templates with Hexagonal Architecture (Ports and Adapters).",
            "    Includes both traditional Spring Boot and reactive WebFlux implementations.",
            "  tags:",
            "    - backstage",
            "    - templates",
            "    - java",
            "    - spring-boot",
            "    - webflux",
            "    - hexagonal-architecture",
            "    - microservices",
            "  links:",
            "    - title: Documentation",
            f"      url: https://github.com/{github_org}/backstage-templates/blob/main/README.md",
            "  annotations:",
            f"    github.com/project-slug: {github_org}/backstage-templates",
            f"    backstage.io/techdocs-ref: url:https://github.com/{github_org}/backstage-templates/tree/main",
            "spec:",
            "  type: template-collection",
            "  owner: platform-team",
            "  lifecycle: production"
        ]
        
        catalog_file = output_path / 'catalog-info.yaml'
        catalog_file.write_text('\n'.join(catalog_content), encoding='utf-8')
        
        # Generate additional files
        first_project = self.projects[0]
        common_vars = {
            'githubOrg': github_org,
            'javaVersion': first_project['project']['dependencies'].get('java', '21'),
            'coverageThreshold': first_project.get('devops', {}).get('ci', {}).get('coverageThreshold', '85')
        }
        
        self._render_template('README.md.mustache', output_path / 'README.md', common_vars)
        self._render_template('mkdocs.yml.mustache', output_path / 'mkdocs.yml', common_vars)
        
        # Copy .gitignore from first project
        first_project_name = self.projects[0]['project']['general']['name']
        source_gitignore = Path('projects') / first_project_name / '.gitignore'
        if source_gitignore.exists():
            shutil.copy(source_gitignore, output_path / '.gitignore')
        
        # catalog-components needs template list
        components_vars = {
            'githubOrg': github_org,
            'templates': [{'folder': t['template_folder']} for t in template_info]
        }
        self._render_template('catalog-components.yaml.mustache', output_path / 'catalog-components.yaml', components_vars)
        
        # Generate docs directory with comprehensive info
        docs_path = output_path / 'docs'
        docs_path.mkdir(exist_ok=True)
        
        # Gather template information
        template_list = []
        for info in template_info:
            proj = next(p for p in self.projects if p['project']['general']['name'] == info['template_folder'])
            template_list.append({
                'name': proj['project']['general']['name'],
                'type': proj['project']['general']['type'],
                'description': proj['project']['general']['description']
            })
        
        # Comprehensive docs variables
        deps = first_project['project']['dependencies']
        devops = first_project.get('devops', {})
        db = first_project.get('database', {})
        maven = first_project.get('maven', {})
        
        docs_vars = {
            'githubOrg': github_org,
            'templates': template_list,
            'javaVersion': deps.get('java', '21'),
            'springBootVersion': deps.get('springBoot', '3.2.5'),
            'mapstructVersion': deps.get('mapstruct', '1.5.5.Final'),
            'lombokVersion': deps.get('lombok', '1.18.30'),
            'springdocVersion': deps.get('springdoc', '2.1.0'),
            'postgresqlVersion': deps.get('postgresql', '42.7.3'),
            'flywayVersion': deps.get('flywayDatabasePostgresql', '10.10.0'),
            'h2Version': deps.get('h2', '2.2.224'),
            'mavenCompilerVersion': deps.get('mavenCompiler', '3.11.0'),
            'mavenSurefireVersion': deps.get('mavenSurefire', '3.2.5'),
            'jacocoVersion': deps.get('jacoco', '0.8.11'),
            'lombokMapstructBindingVersion': deps.get('lombokMapstructBinding', '0.2.0'),
            'mavenWrapperVersion': maven.get('wrapperVersion', '3.3.3'),
            'coverageThreshold': devops.get('ci', {}).get('coverageThreshold', '85'),
            'javaDistribution': devops.get('ci', {}).get('javaDistribution', 'temurin'),
            'mavenOpts': devops.get('ci', {}).get('mavenOpts', '-Xmx1024m'),
            'artifactRetentionDays': devops.get('ci', {}).get('artifactRetentionDays', '30'),
            'postgresqlDbVersion': db.get('version', '15.0'),
            'license': first_project['project']['general'].get('license', 'MIT')
        }
        
        self._render_template('docs-index.md.mustache', docs_path / 'index.md', docs_vars)
        
        print(f"\n📋 Root catalog generated: {catalog_file}")
        print(f"📄 Additional files: README.md, mkdocs.yml, catalog-components.yaml, docs/index.md")
    
    def _generate_type_docs(self, output_path: Path):
        """Generate springboot-service and webflux-service documentation folders."""
        first_project = self.projects[0]
        deps = first_project['project']['dependencies']
        
        types = [
            {
                'folder': 'springboot-service',
                'title': 'Spring Boot Service Template',
                'description': 'Spring Boot microservice template with hexagonal architecture',
                'stackName': 'Spring Boot',
                'dbType': 'JPA con PostgreSQL/MySQL/H2'
            },
            {
                'folder': 'webflux-service',
                'title': 'WebFlux Service Template',
                'description': 'Reactive Spring WebFlux microservice template with hexagonal architecture',
                'stackName': 'Spring WebFlux',
                'dbType': 'R2DBC con PostgreSQL/MySQL/H2'
            }
        ]
        
        for type_info in types:
            type_path = output_path / type_info['folder']
            type_path.mkdir(exist_ok=True)
            
            # Generate mkdocs.yml
            mkdocs_vars = {
                'title': type_info['title'],
                'description': type_info['description']
            }
            self._render_template('type-mkdocs.yml.mustache', type_path / 'mkdocs.yml', mkdocs_vars)
            
            # Generate docs/
            docs_path = type_path / 'docs'
            docs_path.mkdir(exist_ok=True)
            
            docs_vars = {
                'title': type_info['title'],
                'stackName': type_info['stackName'],
                'javaVersion': deps.get('java', '21'),
                'springBootVersion': deps.get('springBoot', '3.2.5'),
                'dbType': type_info['dbType']
            }
            
            self._render_template('type-docs-index.md.mustache', docs_path / 'index.md', docs_vars)
            self._render_template('domain-layer.md.mustache', docs_path / 'domain-layer.md', {})
            self._render_template('application-layer.md.mustache', docs_path / 'application-layer.md', {})
            self._render_template('infrastructure-layer.md.mustache', docs_path / 'infrastructure-layer.md', {})
            
            # Generate catalog-info.yaml
            github_org = self.projects[0].get('devops', {}).get('github', {}).get('organization', 'addon-ai')
            catalog_vars = {
                'templateName': type_info['folder'].replace('-service', ''),
                'description': type_info['description'],
                'stackName': type_info['stackName'],
                'isWebflux': 'webflux' in type_info['folder'],
                'githubOrg': github_org
            }
            self._render_template('type-catalog-info.yaml.mustache', type_path / 'catalog-info.yaml', catalog_vars)
        
        print(f"📚 Type docs: springboot-service/ and webflux-service/ with mkdocs")


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
    
    print("\n✅ Backstage templates generated successfully!")
    print("\n📚 Structure created:")
    print("   • backstage-templates/catalog-info.yaml")
    print("   • backstage-templates/springboot-service/template.yaml")
    print("   • backstage-templates/springboot-service/skeleton/")
    print("   • backstage-templates/webflux-service/template.yaml")
    print("   • backstage-templates/webflux-service/skeleton/")


if __name__ == '__main__':
    main()
