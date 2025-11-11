#!/usr/bin/env python3
import os
import json
import pystache

class BackstageGoldenPathGenerator:
    def __init__(self, projects_dir="projects", output_dir="backstage-templates", config_path="libs/config/params.json"):
        self.projects_dir = projects_dir
        self.output_dir = output_dir
        self.config_path = config_path
        self.templates_dir = os.path.join(os.path.dirname(__file__), "templates")
        
    def generate_all(self):
        """Generate Backstage collection files for all projects"""
        print("🚀 Starting Backstage Collection Generation...")
        
        with open(self.config_path, 'r') as f:
            configs = json.load(f)
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Generate catalog-info.yaml for each project
        for config in configs:
            project_name = config['project']['general']['name']
            self._generate_project_catalog(project_name, config)
        
        # Generate collection files
        self._generate_collection_components(configs)
        self._generate_mkdocs()
        
        print(f"✅ Backstage collection files generated in {self.output_dir}/")
    
    def _generate_project_catalog(self, project_name, config):
        """Generate template.yaml and skeleton/catalog-info.yaml for a project"""
        print(f"  📦 Generating Backstage template for {project_name}...")
        
        project_dir = os.path.join(self.output_dir, project_name)
        skeleton_dir = os.path.join(project_dir, "skeleton")
        os.makedirs(skeleton_dir, exist_ok=True)
        
        # Generate template.yaml
        self._generate_template_yaml(project_name, config, project_dir)
        
        # Generate catalog-info.yaml (for the template itself)
        self._generate_template_catalog_info(project_name, config, project_dir)
        
        # Generate skeleton/catalog-info.yaml (for generated projects)
        self._generate_skeleton_catalog(project_name, config, skeleton_dir)
    
    def _generate_template_yaml(self, project_name, config, project_dir):
        """Generate template.yaml"""
        template_path = os.path.join(self.templates_dir, "template.yaml.mustache")
        with open(template_path, 'r') as f:
            template = f.read()
        
        stack_type = config['project']['general'].get('type', 'springBoot')
        
        data = {
            'template_id': project_name,
            'template_title': config['project']['general']['description'],
            'template_description': config['project']['general']['description'],
            'stack_type': stack_type,
            'default_owner': 'platform-team',
            'default_groupId': config['project']['params']['configOptions']['basePackage'].rsplit('.', 1)[0],
            'default_artifactId': project_name,
            'default_javaVersion': config['devops']['ci'].get('javaVersion', '21'),
            'default_springBootVersion': '3.2.5',
            'default_coverageThreshold': config['devops']['ci'].get('coverageThreshold', '85'),
            'github_org': config['devops']['github']['organization']
        }
        
        output = pystache.render(template, data)
        
        with open(os.path.join(project_dir, "template.yaml"), 'w') as f:
            f.write(output)
    
    def _generate_template_catalog_info(self, project_name, config, project_dir):
        """Generate catalog-info.yaml for the template itself"""
        template_path = os.path.join(self.templates_dir, "template-catalog-info.yaml.mustache")
        with open(template_path, 'r') as f:
            template = f.read()
        
        stack_type = config['project']['general'].get('type', 'springBoot')
        
        data = {
            'template_id': project_name,
            'template_description': config['project']['general']['description'],
            'stack_type': stack_type,
            'github_org': config['devops']['github']['organization'],
            'default_owner': 'platform-team'
        }
        
        output = pystache.render(template, data)
        
        with open(os.path.join(project_dir, "catalog-info.yaml"), 'w') as f:
            f.write(output)
    
    def _generate_skeleton_catalog(self, project_name, config, skeleton_dir):
        """Generate skeleton/catalog-info.yaml"""
        template_path = os.path.join(self.templates_dir, "catalog-info.yaml.mustache")
        with open(template_path, 'r') as f:
            template = f.read()
        
        stack_type = config['project']['general'].get('type', 'springBoot')
        
        data = {
            'stack_type': stack_type,
            'is_webflux': 'webflux' in stack_type.lower(),
            'system_name': 'default-system'
        }
        
        output = pystache.render(template, data)
        
        with open(os.path.join(skeleton_dir, "catalog-info.yaml"), 'w') as f:
            f.write(output)
    
    def _generate_collection_components(self, configs):
        """Generate collection-components.yml"""
        template_path = os.path.join(self.templates_dir, "collection-components.yml.mustache")
        with open(template_path, 'r') as f:
            template = f.read()
        
        targets = []
        for config in configs:
            project_name = config['project']['general']['name']
            targets.append(f"./{project_name}/catalog-info.yaml")
        
        data = {'targets': targets}
        output = pystache.render(template, data)
        
        with open(os.path.join(self.output_dir, "collection-components.yml"), 'w') as f:
            f.write(output)
    
    def _generate_mkdocs(self):
        """Generate mkdocs.yml"""
        template_path = os.path.join(self.templates_dir, "root-mkdocs.yml.mustache")
        if not os.path.exists(template_path):
            return
        
        with open(template_path, 'r') as f:
            template = f.read()
        
        output = pystache.render(template, {})
        
        with open(os.path.join(self.output_dir, "mkdocs.yml"), 'w') as f:
            f.write(output)

if __name__ == "__main__":
    generator = BackstageGoldenPathGenerator()
    generator.generate_all()
