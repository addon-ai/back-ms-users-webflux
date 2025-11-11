#!/usr/bin/env python3
import os
import json

class TechDocsGenerator:
    """Generates TechDocs documentation for each API entity"""
    
    def generate_for_entities(self, project_dir, openapi_files):
        """Generate TechDocs for each entity"""
        entities_dir = os.path.join(project_dir, 'entities')
        
        for openapi_file in openapi_files:
            service_name = openapi_file.replace('.openapi.json', '').replace('Service', '')
            service_name_kebab = ''.join(['-' + c.lower() if c.isupper() else c for c in service_name]).lstrip('-')
            
            entity_dir = os.path.join(entities_dir, service_name_kebab)
            docs_dir = os.path.join(entity_dir, 'docs')
            os.makedirs(docs_dir, exist_ok=True)
            
            openapi_path = os.path.join(project_dir, 'openapi', openapi_file)
            openapi_spec = self._load_openapi(openapi_path)
            
            self._generate_mkdocs(entity_dir, service_name, openapi_spec)
            self._generate_index(docs_dir, service_name, openapi_spec)
            self._generate_api_reference(docs_dir, openapi_spec)
    
    def _load_openapi(self, path):
        """Load OpenAPI specification"""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _generate_mkdocs(self, entity_dir, service_name, openapi_spec):
        """Generate mkdocs.yml for entity"""
        title = openapi_spec.get('info', {}).get('title', f'{service_name} API')
        description = openapi_spec.get('info', {}).get('description', f'API documentation for {service_name}')
        
        content = f"""site_name: '{title} Documentation'
site_description: '{description}'

docs_dir: docs

nav:
  - Introduction: index.md
  - API Reference: api-reference.md

plugins:
  - techdocs-core
"""
        
        with open(os.path.join(entity_dir, 'mkdocs.yml'), 'w') as f:
            f.write(content)
    
    def _generate_index(self, docs_dir, service_name, openapi_spec):
        """Generate docs/index.md"""
        title = openapi_spec.get('info', {}).get('title', f'{service_name} API')
        description = openapi_spec.get('info', {}).get('description', f'API for {service_name}')
        
        # Extract features from paths
        features = self._extract_features(openapi_spec)
        
        content = f"""# {title}

## 📋 Overview

{description}

## ✨ Features

{features}

## 🔐 Authentication

This API uses standard authentication mechanisms. Refer to the OpenAPI specification for detailed authentication requirements.

## ⚡ Rate Limiting

API calls are rate-limited to ensure service stability. Check response headers for current limits.

## 💬 Support

For API support, contact the platform team.
"""
        
        with open(os.path.join(docs_dir, 'index.md'), 'w') as f:
            f.write(content)
    
    def _generate_api_reference(self, docs_dir, openapi_spec):
        """Generate docs/api-reference.md"""
        paths = openapi_spec.get('paths', {})
        
        # Group endpoints by resource
        endpoints_by_resource = self._group_endpoints(paths)
        
        content = """# 📚 API Reference

## OpenAPI Specification

The complete API specification is available in the OpenAPI format. This specification includes:

- All available endpoints
- Request/response schemas
- Authentication requirements
- Error codes and responses

## 🔑 Key Endpoints

"""
        
        for resource, endpoints in endpoints_by_resource.items():
            content += f"\n### {resource}\n"
            for endpoint in endpoints:
                method = endpoint['method'].upper()
                path = endpoint['path']
                desc = endpoint['description']
                content += f"- `{method} {path}` - {desc}\n"
        
        content += "\n\nFor complete details, refer to the OpenAPI specification file.\n"
        
        with open(os.path.join(docs_dir, 'api-reference.md'), 'w') as f:
            f.write(content)
    
    def _extract_features(self, openapi_spec):
        """Extract features from OpenAPI spec"""
        description = openapi_spec.get('info', {}).get('description', '')
        paths = openapi_spec.get('paths', {})
        
        # Try to extract from description
        if 'provides' in description.lower():
            parts = description.split('provides')
            if len(parts) > 1:
                features_text = parts[1].strip()
                features = [f.strip() for f in features_text.split(',')]
                return '\n'.join([f"- **{f.capitalize()}**" for f in features[:5]])
        
        # Fallback: generate from paths
        resources = set()
        for path in paths.keys():
            parts = path.strip('/').split('/')
            if parts:
                resources.add(parts[0].capitalize())
        
        if resources:
            return '\n'.join([f"- **{r} Management**: CRUD operations" for r in sorted(resources)])
        
        return "- **API Operations**: Complete REST API functionality"
    
    def _group_endpoints(self, paths):
        """Group endpoints by resource"""
        grouped = {}
        
        for path, methods in paths.items():
            parts = path.strip('/').split('/')
            resource = parts[0].capitalize() if parts else 'General'
            
            if resource not in grouped:
                grouped[resource] = []
            
            for method, details in methods.items():
                if method in ['get', 'post', 'put', 'delete', 'patch']:
                    desc = details.get('description', details.get('summary', 'No description'))
                    # Truncate long descriptions
                    if len(desc) > 80:
                        desc = desc[:77] + '...'
                    
                    grouped[resource].append({
                        'method': method,
                        'path': path,
                        'description': desc
                    })
        
        return grouped
