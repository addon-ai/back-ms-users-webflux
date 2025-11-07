#!/usr/bin/env python3
"""
Project Processing Script for Code Generation Pipeline
Processes projects based on their type (springBoot or springWebflux)
"""

import json
import sys
import subprocess
import os
import shutil
from pathlib import Path

def clean_projects_directory(projects_dir):
    """Safely clean the projects directory, handling compiled files"""
    if os.path.exists(projects_dir):
        print(f"🗑️  Cleaning projects directory: {projects_dir}")
        try:
            # First, try to clean any Maven target directories
            for root, dirs, files in os.walk(projects_dir):
                if 'target' in dirs:
                    target_path = os.path.join(root, 'target')
                    print(f"   Cleaning Maven target: {target_path}")
                    try:
                        shutil.rmtree(target_path)
                    except Exception as e:
                        print(f"   Warning: Could not clean {target_path}: {e}")
            
            # Now remove the entire projects directory
            shutil.rmtree(projects_dir)
            print("✅ Projects directory cleaned")
        except Exception as e:
            print(f"⚠️  Warning: Could not fully clean projects directory: {e}")
            print("   Continuing with generation...")

def process_projects(config_path, project_root, templates_dir):
    """Process all projects based on their configuration"""
    
    # Load configuration
    with open(config_path, 'r') as f:
        projects_config = json.load(f)
    
    projects_dir = os.path.join(project_root, 'projects')
    
    # Clean projects directory once at the beginning
    clean_projects_directory(projects_dir)
    
    # Separate projects by type
    springboot_projects = []
    webflux_projects = []
    
    for project in projects_config:
        project_type = project.get('project', {}).get('general', {}).get('type', 'springBoot')
        project_name = project.get('project', {}).get('general', {}).get('name', 'unknown')
        
        if project_type == 'springWebflux':
            webflux_projects.append((project_name, project_type))
        else:
            springboot_projects.append((project_name, project_type))
    
    # Process Spring Boot projects first
    if springboot_projects:
        print("🔧 Processing Spring Boot projects...")
        for project_name, project_type in springboot_projects:
            print(f"📦 Processing {project_name} (type: {project_type})")
            try:
                result = subprocess.run([
                    'python3', 
                    os.path.join(project_root, 'libs', 'java-springboot-backend-generator.py')
                ], capture_output=True, text=True, cwd=project_root)
                
                if result.returncode == 0:
                    print(f"✅ Generated {project_name} successfully")
                else:
                    print(f"❌ Error generating {project_name}: {result.stderr}")
                    return False
            except Exception as e:
                print(f"❌ Error generating {project_name}: {e}")
                return False
    
    # Process WebFlux projects
    if webflux_projects:
        print("🔧 Processing Spring WebFlux projects...")
        for project_name, project_type in webflux_projects:
            print(f"📦 Processing {project_name} (type: {project_type})")
            try:
                result = subprocess.run([
                    'python3', 
                    os.path.join(project_root, 'libs', 'java-webflux-backend-generator.py')
                ], capture_output=True, text=True, cwd=project_root)
                
                if result.returncode == 0:
                    print(f"✅ Generated {project_name} successfully")
                else:
                    print(f"❌ Error generating {project_name}: {result.stderr}")
                    return False
            except Exception as e:
                print(f"❌ Error generating {project_name}: {e}")
                return False
    
    return True

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 process_projects.py <config_path> <project_root> <templates_dir>")
        sys.exit(1)
    
    config_path = sys.argv[1]
    project_root = sys.argv[2]
    templates_dir = sys.argv[3]
    
    if not os.path.exists(config_path):
        print(f"❌ Error: Configuration file not found: {config_path}")
        sys.exit(1)
    
    success = process_projects(config_path, project_root, templates_dir)
    
    if not success:
        print("❌ Project processing failed")
        sys.exit(1)
    
    print("✅ All projects processed successfully")

if __name__ == "__main__":
    main()
