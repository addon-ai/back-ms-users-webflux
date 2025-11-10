# Hexagonal Architecture Spring Boot Generator

## Overview

This project generates complete Java Spring Boot applications following **Hexagonal Architecture (Ports and Adapters) principles** from Smithy service definitions. It automatically creates a fully functional backend with proper layer separation, dependency inversion, **GitHub integration**, and **automated pipeline branch management**.

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
- ✅ **CI/CD Workflows** - Automated GitHub Actions with parameterized configuration
- ✅ **Project-Specific Configuration** - Each project uses its own configuration from params.json

### Documentation Generation
- ✅ **OpenAPI Documentation** - Generates PlantUML diagrams from OpenAPI specifications
- ✅ **Architecture Diagrams** - Creates hexagonal architecture component diagrams
- ✅ **Sequence Diagrams** - Generates CRUD sequence diagrams for each service
- ✅ **Real Code Analysis** - Analyzes actual Java controller files for accurate diagrams
- ✅ **Template-Based Diagrams** - Uses Mustache templates for consistent diagram generation
- ✅ **Automated Pipeline** - Integrated documentation generation in code generation pipeline

### GitHub Integration
- ✅ **Repository Management** - Automatically creates private GitHub repositories for generated projects
- ✅ **Branch Management** - Creates develop, test, staging, and main branches
- ✅ **Git History Preservation** - Maintains git history when updating existing projects
- ✅ **Automatic Commits** - Commits and pushes changes to feature branches
- ✅ **Multi-Project Support** - Handles multiple projects in the projects directory
- ✅ **Smart Synchronization** - Detects existing repositories and handles updates appropriately
- ✅ **Project-Specific Configuration** - Each project uses its own GitHub settings from params.json

### Pipeline Branch Management
- ✅ **Automated Branch Creation** - Creates feature branches for each pipeline execution
- ✅ **Branch Limit Management** - Maintains maximum of 10 pipeline branches
- ✅ **Automatic Cleanup** - Removes oldest branches when limit is reached
- ✅ **Smart Commits** - Commits changes with Smithy repository names in message
- ✅ **Configurable Settings** - Branch naming and limits configurable via JSON

### Backstage Integration (Golden Paths)
- ✅ **Software Templates** - Generates Backstage Scaffolder templates from Java projects
- ✅ **Self-Service Platform** - Developers create services via Backstage UI
- ✅ **Automatic Re-Parametrization** - Converts hardcoded values to template variables
- ✅ **Skeleton Generation** - Creates ready-to-use project templates
- ✅ **Platform Engineering** - Complete IDP (Internal Developer Platform) integration

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
│   ├── pyjava-springboot-backend-codegen/         # Core code generation library
│   ├── pyopenapi-docs-generator/       # OpenAPI documentation generator
│   ├── pyarchitect-docs-generator/     # Architecture documentation generator
│   ├── pygithub-integration/           # GitHub integration library
│   │   ├── core/
│   │   │   ├── github_client.py        # GitHub API client
│   │   │   └── git_manager.py          # Git operations manager
│   │   ├── generators/
│   │   │   └── project_sync_generator.py # Project synchronization
│   │   └── .git-backups/               # Git history backups
│   └── config/
│       └── params.json                 # Complete project configuration
├── scripts/
│   ├── code-gen-pipeline.sh            # Complete generation pipeline
│   ├── branch_manager.py               # Pipeline branch management
│   └── pipeline-config.json            # Pipeline configuration
├── projects/                           # Generated Spring Boot projects
├── docs/puml/                          # Generated documentation
└── README.md
```

## Libraries Documentation

### Platform Engineering

#### `py-backstage-goldenpath-gen/`
**Purpose**: Generates Backstage Software Templates (Golden Paths) from Java projects
- **Input**: Generated Java projects from `projects/`
- **Output**: Backstage templates in `backstage-templates/`
- **Process**: Re-parametrizes hardcoded values to Backstage variables
- **Templates**: Creates `template.yaml` and `catalog-info.yaml`
- **Integration**: Complete self-service platform for developers
- **Documentation**: See [BACKSTAGE_INTEGRATION.md](BACKSTAGE_INTEGRATION.md)

### Core Libraries

#### `pyjava-springboot-backend-codegen/`
**Purpose**: Core code generation engine for Spring Boot applications
- **Components**: Generates DTOs, Services, Controllers, Repositories, Entities
- **Architecture**: Implements Hexagonal Architecture patterns
- **Templates**: Uses Mustache templates for consistent code generation
- **Features**: Complete CRUD operations, validation, logging, CI/CD workflows
- **Output**: Fully functional Spring Boot projects with tests

#### `pyopenapi-docs-generator/`
**Purpose**: Generates documentation from OpenAPI specifications
- **Formats**: PlantUML diagrams, Markdown, and TXT documentation
- **Analysis**: Processes OpenAPI specs from Smithy build outputs
- **Categorization**: Separates entities from DTOs based on naming patterns
- **Output**: Comprehensive API documentation in multiple formats

#### `pyarchitect-docs-generator/`
**Purpose**: Creates architectural diagrams from actual Java code
- **Component Diagrams**: Hexagonal architecture visualization
- **Sequence Diagrams**: CRUD operation flows for each service
- **Code Analysis**: Analyzes real Java controller files for accuracy
- **Templates**: Uses Mustache templates for consistent diagram generation
- **Output**: PlantUML diagrams showing system architecture and flows

#### `pygithub-integration/`
**Purpose**: Manages GitHub repositories and Git operations
- **Repository Management**: Creates and updates GitHub repositories
- **Branch Management**: Handles multiple branch strategies
- **History Preservation**: Maintains Git history during updates
- **Project Synchronization**: Syncs multiple projects with their repositories
- **Configuration**: Uses project-specific settings from params.json

### Utility Scripts

#### `scripts/branch_manager.py`
**Purpose**: Manages pipeline execution branches
- **Branch Creation**: Creates timestamped feature branches
- **Limit Management**: Maintains maximum branch count (configurable)
- **Cleanup**: Removes oldest branches automatically
- **Smart Commits**: Commits with Smithy repository names
- **Configuration**: Configurable via pipeline-config.json

#### `scripts/code-gen-pipeline.sh`
**Purpose**: Orchestrates the complete generation pipeline
- **Branch Management**: Creates pipeline branches automatically
- **Code Generation**: Executes all generation steps in sequence
- **Documentation**: Generates all documentation formats
- **GitHub Integration**: Syncs with repositories
- **Commit Management**: Commits all changes with descriptive messages

## GitHub Integration Usage

### Automatic Integration (Recommended)
```bash
# Set GitHub token and run complete pipeline
export GITHUB_TOKEN="your_token"
./scripts/code-gen-pipeline.sh
```

### Manual Operations
```bash
# Sync all projects with GitHub
python3 libs/py-github-integration.py

# Sync specific project
python3 libs/py-github-integration.py project-name

# Create pipeline branch only
python3 scripts/branch_manager.py

# Commit pipeline changes only
python3 scripts/branch_manager.py --commit
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

### Project Configuration (`libs/config/params.json`)
Complete configuration for each project including GitHub settings:
```json
[
  {
    "project": {
      "general": {
        "name": "back-ms-users",
        "description": "Microservice for users management",
        "version": "1.0.0"
      },
      "params": {
        "basePackage": "com.example.userservice",
        "mainClass": "UserServiceApplication"
      }
    },
    "devops": {
      "ci": {
        "javaVersion": "21",
        "coverageThreshold": "85"
      },
      "github": {
        "organization": "addon-ai",
        "repositorySettings": {
          "private": true,
          "description": "Microservice with Hexagonal Architecture"
        },
        "defaultBranches": ["develop", "test", "staging", "main"],
        "gitConfig": {
          "user.name": "Your Name",
          "user.email": "your.email@example.com"
        }
      }
    }
  }
]
```

### Pipeline Configuration (`scripts/pipeline-config.json`)
Branch management settings:
```json
{
  "branchManagement": {
    "branchPrefix": "feature/project_generation",
    "maxBranches": 10,
    "dateFormat": "%Y%m%d_%H%M%S"
  }
}
```

## Development Workflow

1. **Define Service**: Create/modify Smithy service definition
2. **Generate Everything**: Run `./scripts/code-gen-pipeline.sh`
   - Creates new pipeline branch automatically
   - Generates Spring Boot projects with Hexagonal Architecture
   - Creates comprehensive documentation and diagrams
   - Synchronizes with private GitHub repositories
   - Commits all changes with Smithy repository names
3. **Review Changes**: Check pipeline branch for:
   - Generated code and documentation
   - Updated GitHub repositories
   - Automatic commit with descriptive message
4. **Merge Pipeline Branch**: Review and merge pipeline branch to main
5. **Deploy**: Use generated CI/CD workflows in repositories

## Key Components

### GitHub Integration
- **GitHubClient**: GitHub API operations, repository management
- **GitManager**: Git operations, SSH configuration, branch management
- **ProjectSyncGenerator**: Multi-project synchronization with history preservation

### Code Generation
- **CodeGenerator**: Orchestrates complete project generation
- **Template System**: Mustache-based templates for consistent output
- **Component Generators**: Specialized generators for each architecture layer

### Documentation Generation
- **OpenAPI Processor**: Converts Smithy specs to documentation
- **Architecture Analyzer**: Analyzes Java code for diagram generation
- **PlantUML Generator**: Creates visual architecture diagrams

### Pipeline Management
- **BranchManager**: Automated branch lifecycle management
- **Pipeline Orchestrator**: Coordinates all generation steps
- **Configuration Manager**: Handles project-specific settings

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

## Pipeline Execution

### Automatic Branch Management
Each pipeline execution:
1. Creates branch: `feature/project_generation_YYYYMMDD_HHMMSS`
2. Maintains maximum 10 pipeline branches
3. Removes oldest branch when limit reached
4. Commits changes with Smithy repo names: `"Pipeline generation: back-ms-users, back-ms-movies"`

### Generated Outputs
- **Projects**: Complete Spring Boot applications in `projects/`
- **Documentation**: PlantUML diagrams in `docs/puml/`
- **Schemas**: JSON schemas and fake data in `schemas/`
- **Backstage Templates**: Golden Paths in `backstage-templates/`
- **GitHub Repos**: Private repositories with CI/CD workflows
- **Git History**: Preserved across regenerations

## Extension Points

The system can be extended to:
- Support additional architecture patterns
- Add more documentation formats
- Integrate with other Git providers
- Support custom pipeline steps
- Add deployment automation
- Support additional programming languages

## License

This project is licensed under the MIT License.