#!/usr/bin/env python3
import os
import pystache

class RootGenerator:
    """Generates root-level files for backstage-templates"""
    
    def __init__(self, templates_dir, output_dir):
        self.templates_dir = templates_dir
        self.output_dir = output_dir
    
    def generate_readme(self, configs):
        """Generate README.md"""
        template_path = os.path.join(self.templates_dir, "README.md.mustache")
        with open(template_path, 'r') as f:
            template = f.read()
        
        projects = []
        for config in configs:
            name = config['project']['general']['name']
            description = config['project']['general']['description']
            is_webflux = '-webflux' in name
            projects.append({
                'name': name,
                'description': description,
                'isWebflux': is_webflux
            })
        
        content = pystache.render(template, {'projects': projects})
        
        with open(os.path.join(self.output_dir, "README.md"), 'w') as f:
            f.write(content)
    
    def generate_gitignore(self):
        """Generate .gitignore"""
        template_path = os.path.join(self.templates_dir, "skeleton-gitignore.mustache")
        with open(template_path, 'r') as f:
            template = f.read()
        
        with open(os.path.join(self.output_dir, ".gitignore"), 'w') as f:
            f.write(template)
    
    def generate_org_yml(self):
        """Generate org.yml"""
        org_content = """---
# https://backstage.io/docs/features/software-catalog/descriptor-format#kind-user
apiVersion: backstage.io/v1alpha1
kind: User
metadata:
  name: admin
spec:
  memberOf: [guests, platform-team]
---
# https://backstage.io/docs/features/software-catalog/descriptor-format#kind-group
apiVersion: backstage.io/v1alpha1
kind: Group
metadata:
  name: platform-team
spec:
  type: team
  children: []
"""
        with open(os.path.join(self.output_dir, "org.yml"), 'w') as f:
            f.write(org_content)
    
    def generate_systems_yml(self, systems):
        """Generate systems.yml"""
        systems_list = sorted(systems)
        systems_content = []
        
        for system_name, base_name in systems_list:
            description = f"{base_name.replace('-', ' ').title()} management system"
            system_yaml = f"""apiVersion: backstage.io/v1alpha1
kind: System
metadata:
  name: {system_name}
  description: {description}
spec:
  owner: platform-team"""
            systems_content.append(system_yaml)
        
        full_content = "\\n---\\n".join(systems_content) + "\\n"
        
        with open(os.path.join(self.output_dir, "systems.yml"), 'w') as f:
            f.write(full_content)
    
    def generate_collection_components(self, github_org):
        """Generate collection-components.yml"""
        collection_content = f"""apiVersion: backstage.io/v1alpha1
kind: Location
metadata:
  name: hexagonal-components-location
  description: All template components using wildcard pattern
spec:
  targets:
    - https://github.com/{github_org}/backstage-templates/blob/main/*/catalog-info.yml
"""
        with open(os.path.join(self.output_dir, "collection-components.yml"), 'w') as f:
            f.write(collection_content)
    
    def generate_entities_location(self, github_org):
        """Generate entities-location.yml"""
        entities_location_content = f"""apiVersion: backstage.io/v1alpha1
kind: Location
metadata:
  name: backstage-entities-wildcard
  description: All entities using wildcard pattern
spec:
  targets:
    - https://github.com/{github_org}/backstage-templates/blob/main/*/entities/*/*-entity.yml
"""
        with open(os.path.join(self.output_dir, "entities-location.yml"), 'w') as f:
            f.write(entities_location_content)
    
    def generate_dependencies_file(self, all_dependencies):
        """Generate single dependencies.yml with unique dependencies by version only"""
        resources = []
        seen = set()
        
        dep_mapping = {
            'java': ('Java Runtime Environment', 'runtime', ['java', 'runtime']),
            'springBoot': ('Spring Boot Framework', 'library', ['spring-boot', 'framework']),
            'springWebflux': ('Spring WebFlux', 'library', ['spring-webflux', 'reactive']),
            'springDataR2dbc': ('Spring Data R2DBC', 'library', ['spring-data', 'r2dbc']),
            'r2dbcPostgresql': ('R2DBC PostgreSQL Driver', 'database-driver', ['r2dbc', 'postgresql']),
            'r2dbcH2': ('R2DBC H2 Driver', 'database-driver', ['r2dbc', 'h2']),
            'mapstruct': ('MapStruct mapping library', 'library', ['mapstruct', 'mapping']),
            'lombok': ('Lombok code generation library', 'library', ['lombok', 'codegen']),
            'postgresql': ('PostgreSQL JDBC Driver', 'database-driver', ['postgresql', 'database']),
            'h2': ('H2 Database Engine', 'database-driver', ['h2', 'database']),
            'springdoc': ('SpringDoc OpenAPI library', 'library', ['springdoc', 'openapi']),
            'springdocWebflux': ('SpringDoc OpenAPI WebFlux', 'library', ['springdoc', 'webflux']),
            'reactorTest': ('Reactor Test', 'library', ['reactor', 'testing']),
            'mavenCompiler': ('Maven Compiler Plugin', 'library', ['maven', 'compiler']),
            'mavenSurefire': ('Maven Surefire Plugin', 'library', ['maven', 'testing']),
            'lombokMapstructBinding': ('Lombok MapStruct Binding', 'library', ['lombok', 'mapstruct']),
            'jacoco': ('JaCoCo Code Coverage', 'library', ['jacoco', 'testing']),
            'flywayDatabasePostgresql': ('Flyway Database Migration', 'library', ['flyway', 'database'])
        }
        
        for base_name, (deps, system_name) in all_dependencies.items():
            for key, version in deps.items():
                if key in dep_mapping:
                    desc, res_type, tags = dep_mapping[key]
                    version_formatted = version.replace('.', '-').replace('Final', '').strip('-')
                    resource_name = f"{key.lower()}-{version_formatted}"
                    
                    if resource_name not in seen:
                        seen.add(resource_name)
                        tags_yaml = '\n'.join([f"    - {tag}" for tag in tags])
                        resources.append(f"""apiVersion: backstage.io/v1alpha1
kind: Resource
metadata:
  name: {resource_name}
  description: {desc} version {version}
  tags:
{tags_yaml}
spec:
  type: {res_type}
  owner: platform-team""")
        
        content = '\n---\n'.join(resources) + '\n'
        with open(os.path.join(self.output_dir, "dependencies.yml"), 'w') as f:
            f.write(content)
