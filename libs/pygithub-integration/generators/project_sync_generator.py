import os
import sys
import tempfile
import shutil
import subprocess
from typing import List, Dict

# Add the parent directory to the path to import other libraries
libs_dir = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.append(libs_dir)
sys.path.append(os.path.join(libs_dir, 'pyjava-backend-codegen'))

from core.github_client import GitHubClient
from core.git_manager import GitManager
# CodeGenerator import will be handled dynamically when needed

class ProjectSyncGenerator:
    def __init__(self, github_token: str = None):
        self.github_client = GitHubClient(github_token)
        # Get project root relative to this file
        self.project_root = os.path.join(os.path.dirname(__file__), '..', '..', '..')
        self.projects_dir = os.path.join(self.project_root, "projects")
        self.default_branches = ["develop", "test", "staging", "main"]
    
    def backup_existing_projects(self):
        """Backup Git history for projects that exist on GitHub"""
        if not os.path.exists(self.projects_dir):
            print(f"Projects directory '{self.projects_dir}' not found")
            return
        
        # Get owner from config or user info
        config = self.github_client.config
        owner = config.get('github', {}).get('organization')
        
        if not owner:
            # Fallback to user login if no organization configured
            user_info = self.github_client.get_user()
            owner = user_info.get('login')
            
            if not owner:
                print(f"Failed to get GitHub user info")
                return
        
        projects = [d for d in os.listdir(self.projects_dir) 
                   if os.path.isdir(os.path.join(self.projects_dir, d))]
        
        backup_base_dir = self.github_client.config.get('projects', {}).get('backupDirectory', '.git-backups')
        os.makedirs(backup_base_dir, exist_ok=True)
        
        for project_name in projects:
            project_path = os.path.join(self.projects_dir, project_name)
            git_manager = GitManager(project_path)
            
            # Check if repository exists on GitHub
            if self.github_client.repository_exists(owner, project_name):
                if git_manager.has_git_repo():
                    backup_path = os.path.join(backup_base_dir, f"{project_name}_git")
                    git_manager.backup_git_history(backup_path)
                    print(f"✅ Backed up Git history for {project_name}")
                else:
                    print(f"⚠️  {project_name} exists on GitHub but has no local .git")
            else:
                print(f"ℹ️  {project_name} not found on GitHub, will be created")
    
    def sync_all_projects(self):
        """Sync all projects in the projects directory"""
        if not os.path.exists(self.projects_dir):
            print(f"Projects directory '{self.projects_dir}' not found")
            return
        
        projects = [d for d in os.listdir(self.projects_dir) 
                   if os.path.isdir(os.path.join(self.projects_dir, d))]
        
        for project_name in projects:
            print(f"Processing project: {project_name}")
            self.sync_project(project_name)
    
    def sync_project(self, project_name: str):
        """Sync a single project with GitHub"""
        project_path = os.path.join(self.projects_dir, project_name)
        git_manager = GitManager(project_path)
        
        # Get owner from config or user info
        config = self.github_client.config
        owner = config.get('github', {}).get('organization')
        
        if not owner:
            # Fallback to user login if no organization configured
            user_info = self.github_client.get_user()
            owner = user_info.get('login')
            
            if not owner:
                print(f"Failed to get GitHub user info")
                return
        
        # Check if repository exists
        repo_exists = self.github_client.repository_exists(owner, project_name)
        
        if not repo_exists:
            print(f"Repository {project_name} doesn't exist. Creating...")
            self._create_new_repository(project_name, project_path, git_manager)
        else:
            print(f"Repository {project_name} exists. Updating...")
            self._update_existing_repository(project_name, project_path, git_manager)
    
    def _create_new_repository(self, project_name: str, project_path: str, git_manager: GitManager):
        """Create new repository and push project"""
        # Create repository on GitHub
        repo_data = self.github_client.create_repository(
            project_name, 
            f"Generated Spring Boot project: {project_name}"
        )
        
        remote_url = repo_data.get('clone_url')
        if not remote_url:
            print(f"Failed to create repository {project_name}")
            return
        
        # Initialize git repository
        git_manager.init_repository(project_name)
        
        # Initial commit and push to main branch
        git_manager.initial_commit_and_push("Initial commit: Generated Spring Boot project")
        
        # Create and push additional branches
        git_manager.create_branches(self.default_branches[:-1])  # Exclude main as it already exists
        
        print(f"Successfully created and pushed {project_name}")
    
    def _update_existing_repository(self, project_name: str, project_path: str, git_manager: GitManager):
        """Update existing repository preserving git history"""
        # Check for existing backup first
        backup_base_dir = self.github_client.config.get('projects', {}).get('backupDirectory', '.git-backups')
        backup_path = os.path.join(backup_base_dir, f"{project_name}_git")
        
        backup_dir = None
        if os.path.exists(backup_path):
            backup_dir = backup_path
            print(f"Using existing backup from {backup_dir}")
        elif git_manager.has_git_repo():
            backup_dir = tempfile.mkdtemp()
            git_manager.backup_git_history(backup_dir)
            print(f"Backed up git history to {backup_dir}")
        
        try:
            # Regenerate project using code generator
            self._regenerate_project(project_name, project_path)
            
            # Restore git history
            if backup_dir:
                git_manager.restore_git_history(backup_dir)
                print("Restored git history")
            
            # Create feature branch and push changes
            feature_branch = git_manager.get_feature_branch_name()
            commit_message = f"Auto-generated update: {feature_branch}"
            git_manager.commit_and_push(feature_branch, commit_message)
            
            print(f"Successfully updated {project_name} in branch {feature_branch}")
            
        finally:
            # Clean up temporary backup (but keep permanent backups)
            if backup_dir and backup_dir != backup_path and os.path.exists(backup_dir):
                shutil.rmtree(backup_dir)
    
    def _regenerate_project(self, project_name: str, project_path: str):
        """Regenerate project using the code generator"""
        # Remove existing project content (except .git)
        for item in os.listdir(project_path):
            if item != '.git':
                item_path = os.path.join(project_path, item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)
        
        # Regenerate project by calling the java-backend-generator script
        try:
            # Change to project root directory
            original_cwd = os.getcwd()
            os.chdir(self.project_root)
            
            result = subprocess.run([
                'python3', 
                os.path.join(self.project_root, 'libs', 'java-backend-generator.py'),
                os.path.join(self.project_root, 'libs', 'pyjava-backend-codegen', 'templates')
            ], check=True, capture_output=True, text=True)
            print(f"Regenerated project {project_name}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to regenerate project {project_name}: {e}")
            print(f"Error output: {e.stderr}")
        finally:
            # Restore original working directory
            os.chdir(original_cwd)

def main():
    """Main entry point"""
    # Parse command line arguments
    backup_only = '--backup-only' in sys.argv
    
    # Filter out command flags to get project name
    project_args = [arg for arg in sys.argv[1:] if not arg.startswith('--')]
    
    sync_generator = ProjectSyncGenerator()
    
    if backup_only:
        sync_generator.backup_existing_projects()
    elif project_args:
        project_name = project_args[0]
        sync_generator.sync_project(project_name)
    else:
        sync_generator.sync_all_projects()

if __name__ == "__main__":
    main()