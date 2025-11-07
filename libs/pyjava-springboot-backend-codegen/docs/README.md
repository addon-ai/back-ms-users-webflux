# PyJava Backend Code Generator

## Overview

A modular Python-based code generator that creates complete Java Spring Boot applications following **Hexagonal Architecture (Ports and Adapters)** principles from OpenAPI specifications. The generator produces production-ready microservices with comprehensive test coverage and proper architectural separation.

## Architecture

The generator follows a **component-based architecture** with clear separation of concerns:

```
libs/pyjava-backend-codegen/
├── core/                    # Core orchestration and processing
├── generators/              # Layer-specific code generators  
├── templates/               # Mustache templates by architectural layer
├── utils/                   # Shared utilities and converters
└── docs/                    # Architecture documentation
```

## Core Components

### 1. Core Layer (`core/`)
- **`CodeGenerator`**: Main orchestrator coordinating the entire generation process
- **`ConfigLoader`**: Handles configuration loading and package structure building
- **`OpenApiProcessor`**: Processes OpenAPI specifications and extracts metadata

### 2. Generator Layer (`generators/`)
- **`DtoGenerator`**: Generates Data Transfer Objects from OpenAPI schemas
- **`DomainGenerator`**: Creates domain models and ports (business logic layer)
- **`ApplicationGenerator`**: Builds application services, mappers, and use cases
- **`InfrastructureGenerator`**: Generates adapters, controllers, and persistence layer
- **`TestGenerator`**: Creates comprehensive test suites with 100% coverage
- **`ProjectGenerator`**: Handles project structure and configuration files

### 3. Template Layer (`templates/`)
Organized by architectural layers:
- **`domain/`**: Pure business logic templates
- **`application/`**: Use case implementations and DTOs
- **`infrastructure/`**: External adapters and configuration
- **`project/`**: Project setup and build files
- **`tests/`**: Comprehensive test templates

### 4. Utilities Layer (`utils/`)
- **`TemplateRenderer`**: Mustache template processing
- **`FileManager`**: File system operations and directory management
- **`PropertyConverter`**: OpenAPI to Java type conversion with validation

## Generated Architecture

The generator produces applications following **Hexagonal Architecture**:

```
generated-project/
├── domain/                  # Business logic (center of hexagon)
│   ├── model/              # Domain entities
│   └── ports/              # Interfaces (input/output ports)
├── application/            # Use case orchestration
│   ├── dto/                # Data transfer objects
│   ├── service/            # Use case implementations
│   └── mapper/             # Entity transformations
└── infrastructure/         # External adapters
    ├── adapters/           # Input/output adapters
    └── config/             # Framework configuration
```

## Key Features

### 1. **Hexagonal Architecture Compliance**
- **Dependency Rule**: All dependencies point inward toward domain
- **Ports and Adapters**: Clean separation between business logic and external concerns
- **Domain Isolation**: Pure business objects without framework dependencies

### 2. **Comprehensive Code Generation**
- **DTOs**: Request/response objects with validation
- **Domain Models**: Pure business entities
- **Use Cases**: Consolidated business operations
- **Mappers**: MapStruct transformations with proper annotations
- **Controllers**: REST endpoints with proper HTTP mappings
- **Repositories**: JPA persistence with search capabilities
- **Tests**: 100% coverage including edge cases and exception handling

### 3. **Advanced Template Features**
- **Proper Pluralization**: Handles irregular plurals (City → Cities)
- **Type Safety**: Correct BigDecimal vs Double handling
- **MapStruct Integration**: Resolves ambiguous mappings with @IterableMapping
- **Spring Boot 3**: Jakarta EE and modern Spring features
- **Exception Handling**: Comprehensive error management

### 4. **Test Generation Excellence**
- **Complete Coverage**: All methods including catch blocks
- **Edge Case Testing**: Null parameters, exceptions, boundary conditions
- **Spring Integration**: Proper dependency injection in tests
- **Functional Testing**: LoggingUtils with assertDoesNotThrow patterns

## Generation Process

### 1. **OpenAPI Processing**
```python
# Extract schemas, operations, and entities
all_schemas, all_operations, all_entities = self._extract_openapi_data()
```

### 2. **Layer Generation**
```python
# Generate in dependency order (domain → application → infrastructure)
self._generate_domain_layer(all_entities, all_schemas)
self._generate_application_layer(entity_operations, all_entities)  
self._generate_infrastructure_layer(all_entities, all_schemas, entity_operations)
```

### 3. **Test Generation**
```python
# Generate comprehensive test suites
self.test_generator.generate_tests_for_existing_components(self.mustache_context)
```

## Template System

### Mustache Context Variables
- **`entityName`**: Entity name (e.g., "User")
- **`entityNamePlural`**: Proper plural form (e.g., "Cities")
- **`entityVarName`**: Variable name (e.g., "user")
- **`packageName`**: Target package for generated class
- **`basePackage`**: Root package for imports

### Template Organization
```
templates/
├── domain/
│   ├── pojo.mustache              # Domain models
│   └── interface.mustache         # Repository ports
├── application/
│   ├── apiService.mustache        # Use case implementations
│   └── apiMapper.mustache         # MapStruct mappers
├── infrastructure/
│   ├── apiController.mustache     # REST controllers
│   ├── apiRepository.mustache     # JPA repositories
│   └── apiEntity.mustache         # Database entities
└── tests/
    ├── serviceTest.mustache       # Service tests
    ├── mapperTest.mustache        # Mapper tests
    └── repositoryAdapterTest.mustache # Repository tests
```

## Configuration

### Project Configuration
```json
{
  "project": {
    "general": {
      "name": "user-service",
      "version": "1.0.0",
      "description": "User management microservice"
    },
    "params": {
      "configOptions": {
        "basePackage": "com.example.userservice",
        "useSpringBoot3": "true",
        "useJakartaEe": "true"
      }
    }
  }
}
```

### Package Structure
```python
target_packages = {
    'domain_model': 'com.example.userservice.domain.model',
    'domain_ports_input': 'com.example.userservice.domain.ports.input',
    'domain_ports_output': 'com.example.userservice.domain.ports.output',
    'application_service': 'com.example.userservice.application.service',
    'application_dto': 'com.example.userservice.application.dto',
    'application_mapper': 'com.example.userservice.application.mapper',
    'infra_adapters_input_rest': 'com.example.userservice.infrastructure.adapters.input.rest',
    'infra_adapter': 'com.example.userservice.infrastructure.adapters.output.persistence.adapter',
    'infra_entity': 'com.example.userservice.infrastructure.adapters.output.persistence.entity',
    'infra_repository': 'com.example.userservice.infrastructure.adapters.output.persistence.repository'
}
```

## Usage

### Basic Generation
```python
from core.code_generator import CodeGenerator

generator = CodeGenerator(config_path, templates_dir, project_config)
generator.generate_complete_project()
```

### Custom Generation
```python
# Generate specific layers
generator._generate_domain_layer(entities, schemas)
generator._generate_application_layer(operations, entities)
generator._generate_infrastructure_layer(entities, schemas, operations)
```

## Best Practices

### 1. **Template Development**
- Use semantic variable names (`entityNamePlural` vs `entityNames`)
- Handle edge cases (null values, empty collections)
- Include proper imports and annotations

### 2. **Type Handling**
- Distinguish BigDecimal from Double based on OpenAPI format
- Use proper Java type mappings for validation
- Handle temporal types correctly (OffsetDateTime vs String)

### 3. **Test Coverage**
- Test all code paths including exception handling
- Use Spring Boot test configuration for integration
- Include null parameter coverage tests

## Extension Points

The generator can be extended by:

1. **Adding New Templates**: Create templates in appropriate layer directories
2. **Custom Generators**: Implement new generator classes following existing patterns
3. **Type Converters**: Extend PropertyConverter for new OpenAPI types
4. **Template Variables**: Add context variables in generator classes

## Dependencies

### Runtime Dependencies
- **Python 3.8+**
- **pystache**: Mustache template engine
- **pathlib**: File system operations

### Generated Project Dependencies
- **Spring Boot 3.x**: Web, Data JPA, Validation
- **Jakarta EE**: Modern Java enterprise APIs
- **MapStruct**: Bean mapping with Spring integration
- **Lombok**: Boilerplate reduction
- **JUnit 5**: Testing framework
- **AssertJ**: Fluent assertions

## Troubleshooting

### Common Issues

1. **Template Rendering Errors**
   - Check variable names in context
   - Verify template syntax
   - Ensure all required variables are provided

2. **Type Conversion Issues**
   - Verify OpenAPI schema format fields
   - Check PropertyConverter mappings
   - Validate generated Java types

3. **Test Compilation Errors**
   - Ensure proper Spring Boot test configuration
   - Check import statements
   - Verify mock configurations

### Debug Mode
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

1. Follow existing architectural patterns
2. Add comprehensive tests for new features
3. Update documentation for new components
4. Ensure generated code follows Hexagonal Architecture principles