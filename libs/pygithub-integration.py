#!/usr/bin/env python3
"""
GitHub Integration Library - Main Entry Point
Manages GitHub repositories for generated Spring Boot projects
"""

import sys
import os

# Add the pygithub-integration directory to the path
current_dir = os.path.dirname(__file__)
pygithub_dir = os.path.join(current_dir, 'pygithub-integration')
sys.path.insert(0, pygithub_dir)

from generators.project_sync_generator import ProjectSyncGenerator

def main():
    """Main entry point for GitHub integration"""
    print("=== GitHub Integration Library ===")
    
    # Parse command line arguments
    backup_only = '--backup-only' in sys.argv
    sync_mode = '--sync' in sys.argv
    
    if backup_only:
        print("Backing up Git history for existing GitHub repositories...")
    elif sync_mode:
        print("Synchronizing projects with GitHub repositories...")
    else:
        print("Synchronizing projects with GitHub repositories...")
    
    try:
        sync_generator = ProjectSyncGenerator()
        
        # Filter out command flags to get project name
        project_args = [arg for arg in sys.argv[1:] if not arg.startswith('--')]
        
        if backup_only:
            sync_generator.backup_existing_projects()
        elif project_args:
            project_name = project_args[0]
            print(f"Syncing specific project: {project_name}")
            sync_generator.sync_project(project_name)
        else:
            print("Syncing all projects in 'projects' directory")
            sync_generator.sync_all_projects()
            
        print("GitHub integration completed successfully!")
        
    except Exception as e:
        print(f"Error during GitHub integration: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()