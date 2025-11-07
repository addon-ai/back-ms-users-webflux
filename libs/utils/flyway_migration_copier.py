#!/usr/bin/env python3

import json
import os
import shutil
from pathlib import Path

def copy_flyway_migrations():
    """Copy and merge Flyway SQL scripts to project migration directories"""
    
    # Get project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    
    # Load configuration
    config_path = project_root / "libs" / "config" / "params.json"
    
    with open(config_path, 'r') as f:
        projects = json.load(f)
    
    for project_config in projects:
        project_name = project_config['project']['general']['name']
        project_folder = project_config['project']['general']['folder']
        sgbd = project_config['database']['sgbd']
        flyway_scripts = project_config['database']['flywayScripts']
        
        # Source directory for SQL scripts
        sql_source_dir = project_root / "sql" / sgbd
        
        # Target project directory
        project_dir = project_root / "projects" / project_folder
        
        if not project_dir.exists():
            print(f"⚠️  Project directory not found: {project_dir}")
            continue
            
        # Create migration directories
        main_migration_dir = project_dir / "src" / "main" / "resources" / "db" / "migration"
        test_migration_dir = project_dir / "src" / "test" / "resources" / "db" / "migration"
        
        main_migration_dir.mkdir(parents=True, exist_ok=True)
        test_migration_dir.mkdir(parents=True, exist_ok=True)
        
        # Merge SQL scripts into single V1__ file
        merged_content = []
        
        for script_name in flyway_scripts:
            script_path = sql_source_dir / script_name
            
            if script_path.exists():
                with open(script_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        merged_content.append(f"-- {script_name}")
                        merged_content.append(content)
                        merged_content.append("")  # Empty line separator
            else:
                print(f"⚠️  SQL script not found: {script_path}")
        
        if merged_content:
            # Create Flyway versioned migration file
            flyway_filename = "V1__initial_schema.sql"
            merged_sql = "\n".join(merged_content)
            
            # Write to main migration directory
            main_migration_file = main_migration_dir / flyway_filename
            with open(main_migration_file, 'w', encoding='utf-8') as f:
                f.write(merged_sql)
            
            # Copy to test migration directory
            test_migration_file = test_migration_dir / flyway_filename
            shutil.copy2(main_migration_file, test_migration_file)
            
            print(f"✅ Created Flyway migration for {project_name}: {flyway_filename}")
            print(f"   📁 Main: {main_migration_file}")
            print(f"   📁 Test: {test_migration_file}")
        else:
            print(f"⚠️  No SQL content found for project: {project_name}")

if __name__ == "__main__":
    copy_flyway_migrations()