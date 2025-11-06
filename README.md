# Hexagonal Architecture Spring Boot Generator

## Overview

This project generates complete Java Spring Boot applications following **Hexagonal Architecture (Ports and Adapters) principles** from Smithy service definitions. It automatically creates a fully functional backend with proper layer separation, dependency inversion, and **GitHub integration**.

## Features

### Core Generation
- ✅ **Hexagonal Architecture Structure** with Domain, Application, and Infrastructure layers
- ✅ **Smithy Integration** - Generates OpenAPI specs from Smithy definitions
- ✅ **Complete Code Generation** - DTOs, Services, Controllers, Repositories, Entities
- ✅ **Comprehensive Test Coverage** - Unit tests with 100% code coverage including edge cases
- ✅ **Component-Based Generator** - Modular architecture with specialized generators
- ✅ **Dependency Inversion** - All dependencies point toward the domain layer
- ✅ **Spring Boot 3** with Jakarta EE support
- ✅ **MapStruct** for entity transformations
- ✅ **JPA/Hibernate** for persistence
- ✅ **Bean Validation** with proper annotations
- ✅ **Lombok** for boilerplate reduction
- ✅ **Logging Utilities** with MDC support and comprehensive test coverage

### Documentation Generation
- ✅ **OpenAPI Documentation** - Generates PlantUML diagrams from OpenAPI specifications
- ✅ **Architecture Diagrams** - Creates hexagonal architecture component diagrams
- ✅ **Sequence Diagrams** - Generates CRUD sequence diagrams for each service
- ✅ **Real Code Analysis** - Analyzes actual Java controller files for accurate diagrams
- ✅ **Template-Based Diagrams** - Uses Mustache templates for consistent diagram generation
- ✅ **Automated Pipeline** - Integrated documentation generation in code generation pipeline

### GitHub Integration
- ✅ **Repository Management** - Automatically creates GitHub repositories for generated projects
- ✅ **Branch Management** - Creates develop, test, staging, and main branches
- ✅ **Git History Preservation** - Maintains git history when updating existing projects
- ✅ **Automatic Commits** - Commits and pushes changes to feature branches
- ✅ **Multi-Project Support** - Handles multiple projects in the projects directory
- ✅ **Smart Synchronization** - Detects existing repositories and handles updates appropriately

## Quick Start

### 1. Install Dependencies

```bash
# Install Python dependencies
poetry install

# Install Java and Maven (if not already installed)
brew install maven
sdk install java 21.0.2-tem
sdk use java 21.0.2-tem

# Install additional Python packages for GitHub integration
pip3 install requests
```

### 2. Set up GitHub Integration (Optional)

```bash
# Set your GitHub personal access token
export GITHUB_TOKEN="your_github_token_here"

# Or add to your shell profile (.bashrc, .zshrc, etc.)
echo 'export GITHUB_TOKEN="your_github_token_here"' >> ~/.zshrc
```

### 3. Generate Project

```bash
# Make script executable
chmod +x scripts/code-gen-pipeline.sh

# Run complete pipeline (includes GitHub integration if token is set)
./scripts/code-gen-pipeline.sh
```

### 4. Run Generated Project

```bash
cd projects/[project-name]

# Build and run
mvn spring-boot:run
```

### 5. Test API

```bash
# Create user
curl -X POST http://localhost:8080/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "password123",
    "firstName": "John",
    "lastName": "Doe"
  }'

# Get user
curl http://localhost:8080/users/{userId}

# List users
curl http://localhost:8080/users
```

## Prerequisites

### System Requirements
- **Java 21** (recommended with SDKMAN)
- **Maven 3.8+**
- **Python 3.6+**
- **Git** (for GitHub integration)
- **GitHub Personal Access Token** (for GitHub integration)

### GitHub Setup
1. Create a GitHub Personal Access Token:
   - Go to GitHub Settings → Developer settings → Personal access tokens
   - Generate new token with `repo` permissions
   - Set as environment variable: `export GITHUB_TOKEN="your_token"`

### Java Installation with SDKMAN
```bash
sdk install java 21.0.2-tem
sdk use java 21.0.2-tem
```

### Maven Installation
```bash
# Using Homebrew (macOS)
brew install maven

# Using SDKMAN
sdk install maven

# Verify installation
mvn -version
```

### Python Dependencies
```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
poetry install

# Or install manually
pip3 install pystache requests
```

## Project Structure

```
boiler-plate-code-gen/
├── libs/
│   ├── pyjava-backend-codegen/         # Core code generation library
│   ├── openapi-docs-generator/         # OpenAPI documentation generator
│   ├── pyarchitect-docs-generator/     # Architecture documentation generator
│   ├── pygithub-integration/           # GitHub integration library
│   │   ├── core/
│   │   │   ├── github_client.py        # GitHub API client
│   │   │   └── git_manager.py          # Git operations manager
│   │   └── generators/
│   │       └── project_sync_generator.py # Project synchronization
│   └── config/
│       ├── params.json                 # Project configuration
│       └── github-config.json          # GitHub integration settings
├── scripts/
│   └── code-gen-pipeline.sh            # Complete generation pipeline
├── projects/                           # Generated Spring Boot projects
├── docs/puml/                          # Generated documentation
└── README.md
```

## GitHub Integration Usage

### Automatic Integration (Recommended)
```bash
# Set GitHub token and run complete pipeline
export GITHUB_TOKEN="your_token"
./scripts/code-gen-pipeline.sh
```

### Manual Integration
```bash
# Sync all projects
python3 libs/pygithub-integration.py

# Sync specific project
python3 libs/pygithub-integration.py project-name
```

### GitHub Integration Features

#### New Repository Creation
- Creates GitHub repository with project name
- Initializes with main branch
- Creates develop, test, staging branches
- Pushes initial project code

#### Existing Repository Updates
- Backs up existing .git history
- Regenerates project with latest templates
- Restores git history
- Creates feature branch with timestamp
- Commits and pushes changes

#### Branch Naming Convention
- Feature branches: `feature/push_automatic_YYYYMMDD_HHMMSS`
- Default branches: `main`, `develop`, `test`, `staging`

## Generated Architecture

The generator creates a complete Hexagonal Architecture project with proper package structure and GitHub integration:

```
projects/[project-name]/
├── .git/                               # Git repository (if GitHub integration enabled)
├── .github/workflows/                  # CI/CD workflows
├── src/main/java/com/example/service/
│   ├── domain/                         # Pure domain layer
│   ├── application/                    # Application services and DTOs
│   └── infrastructure/                 # Controllers and adapters
├── src/test/java/                      # Comprehensive test suite
└── pom.xml                            # Maven configuration
```

## Configuration

### GitHub Configuration (`libs/config/github-config.json`)
```json
{
  "github": {
    "defaultBranches": ["develop", "test", "staging", "main"],
    "repositorySettings": {
      "private": false,
      "autoInit": false
    }
  }
}
```

### Project Configuration (`libs/config/params.json`)
```json
[
  {
    "project": {
      "general": {
        "name": "back-ms-users",
        "basePackage": "com.example.userservice"
      }
    }
  }
]
```

## Development Workflow with GitHub Integration

1. **Define Service**: Create/modify Smithy service definition
2. **Generate Everything**: Run `./scripts/code-gen-pipeline.sh`
   - Generates Spring Boot projects
   - Creates documentation and diagrams
   - Synchronizes with GitHub repositories
3. **Review Changes**: Check GitHub repositories for:
   - New repositories (if created)
   - Feature branches with updates (if existing)
4. **Create Pull Requests**: Review and merge feature branches
5. **Deploy**: Use CI/CD workflows in generated repositories

## GitHub Integration Components

### GitHubClient (`libs/pygithub-integration/core/github_client.py`)
- Repository existence checking
- Repository creation
- User authentication

### GitManager (`libs/pygithub-integration/core/git_manager.py`)
- Git repository initialization
- Branch creation and management
- Commit and push operations
- Git history backup/restore

### ProjectSyncGenerator (`libs/pygithub-integration/generators/project_sync_generator.py`)
- Multi-project synchronization
- Smart repository detection
- Code regeneration with history preservation

## Troubleshooting

### GitHub Integration Issues

1. **Authentication Errors**
   ```bash
   # Verify token is set
   echo $GITHUB_TOKEN
   
   # Test GitHub API access
   curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user
   ```

2. **Repository Creation Fails**
   - Check token permissions (needs `repo` scope)
   - Verify repository name doesn't already exist
   - Check GitHub API rate limits

3. **Git Push Fails**
   - Ensure git is configured: `git config --global user.name "Your Name"`
   - Check repository permissions
   - Verify remote URL is correct

4. **Project Regeneration Issues**
   - Ensure code generator templates are available
   - Check project structure matches expected format
   - Verify backup/restore process

### Common Solutions
```bash
# Reset git configuration
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Clear git cache
git rm -r --cached .
git add .

# Force push (use with caution)
git push --force-with-lease origin branch-name
```

## Extension Points

The GitHub integration can be extended to:
- Support other Git providers (GitLab, Bitbucket)
- Add pull request automation
- Integrate with CI/CD platforms
- Add deployment automation
- Support custom branch strategies

## Contributing

1. Fork the repository
2. Create feature branch
3. Add/modify GitHub integration components
4. Test with sample projects
5. Submit pull request

## License

This project is licensed under the MIT License.