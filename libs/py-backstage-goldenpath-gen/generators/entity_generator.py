#!/usr/bin/env python3
import os
import json

class EntityGenerator:
    """Generates entity files for APIs"""
    
    def generate(self, project_name, project_dir, openapi_files):
        """Generate individual entity files for each OpenAPI spec"""
        is_webflux = '-webflux' in project_name
        base_name = project_name.replace('-webflux', '').replace('back-ms-', '')
        system_name = f"{base_name}-system"
        
        entities_dir = os.path.join(project_dir, 'entities')
        os.makedirs(entities_dir, exist_ok=True)
        
        for openapi_file in openapi_files:
            service_name = openapi_file.replace('.openapi.json', '').replace('Service', '')
            service_name_kebab = ''.join(['-' + c.lower() if c.isupper() else c for c in service_name]).lstrip('-')
            
            api_name = f"{service_name_kebab}-reactive-api" if is_webflux else f"{service_name_kebab}-api"
            
            # Create entity subdirectory
            entity_dir = os.path.join(entities_dir, service_name_kebab)
            os.makedirs(entity_dir, exist_ok=True)
            
            openapi_path = os.path.join(project_dir, 'openapi', openapi_file)
            description = f"API for {service_name}"
            
            try:
                with open(openapi_path, 'r') as f:
                    openapi_spec = json.load(f)
                    description = openapi_spec.get('info', {}).get('description', description)
            except:
                pass
            
            entity_content = f"""apiVersion: backstage.io/v1alpha1
kind: API
metadata:
  name: {api_name}
  description: {description}
  annotations:
    backstage.io/techdocs-ref: dir:.
spec:
  type: openapi
  lifecycle: experimental
  owner: platform-team
  system: {system_name}
  definition:
    $text: ../../openapi/{openapi_file}
"""
            
            entity_filename = f"{service_name_kebab}-entity.yml"
            with open(os.path.join(entity_dir, entity_filename), 'w') as f:
                f.write(entity_content)
    
    def get_provides_apis(self, project_name, project_dir):
        """Get list of API names that this component provides"""
        is_webflux = '-webflux' in project_name
        entities_dir = os.path.join(project_dir, 'entities')
        apis = []
        
        if os.path.exists(entities_dir):
            for item in os.listdir(entities_dir):
                item_path = os.path.join(entities_dir, item)
                if os.path.isdir(item_path):
                    service_name = item
                    api_name = f"{service_name}-reactive-api" if is_webflux else f"{service_name}-api"
                    apis.append(api_name)
        
        return apis
