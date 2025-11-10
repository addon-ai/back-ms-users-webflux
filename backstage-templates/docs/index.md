# Hexagonal Architecture Templates

Welcome to the Hexagonal Architecture Templates documentation.

## Overview

This repository provides Backstage Software Templates for creating Spring Boot microservices following Hexagonal Architecture principles (Ports and Adapters pattern).

## Available Templates

### back-ms-users
**Type**: springBoot  
**Description**: Microservice for users management

### back-ms-movies
**Type**: springBoot  
**Description**: Microservice for movie rental management

### back-ms-users-webflux
**Type**: springWebflux  
**Description**: Reactive microservice for users management with Spring WebFlux

### back-ms-movies-webflux
**Type**: springWebflux  
**Description**: Reactive microservice for movie rental management with Spring WebFlux


## Technology Stack

### Core Dependencies

| Dependency | Version |
|------------|---------|
| Java | 21 |
| Spring Boot | 3.2.5 |
| MapStruct | 1.5.5.Final |
| Lombok | 1.18.30 |
| Springdoc OpenAPI | 2.1.0 |

### Database

| Component | Version |
|-----------|---------|
| PostgreSQL | 42.7.3 |
| Flyway | 10.10.0 |
| H2 (Testing) | 2.2.224 |

### Build Tools

| Tool | Version |
|------|---------|
| Maven Compiler | 3.11.0 |
| Maven Surefire | 3.2.5 |
| Jacoco | 0.8.11 |

### Additional Libraries

- **Lombok-MapStruct Binding**: 0.2.0
- **Maven Wrapper**: 3.3.3

## Architecture

All templates follow the Hexagonal Architecture pattern with three main layers:

### Domain Layer
- **Purpose**: Core business logic and entities
- **Dependencies**: None (pure domain)
- **Components**: Domain models, business rules, domain exceptions

### Application Layer
- **Purpose**: Use cases and application services
- **Dependencies**: Domain layer only
- **Components**: 
  - Input Ports (use case interfaces)
  - Output Ports (repository interfaces)
  - DTOs (Data Transfer Objects)
  - MapStruct mappers

### Infrastructure Layer
- **Purpose**: External adapters and technical implementations
- **Dependencies**: Application and Domain layers
- **Components**:
  - REST Controllers (input adapters)
  - JPA/R2DBC Repositories (output adapters)
  - Database entities
  - Configuration classes

## Features

### Code Quality
- **Test Coverage**: Minimum 85% enforced by Jacoco
- **Code Generation**: MapStruct for type-safe mappings
- **Boilerplate Reduction**: Lombok annotations

### Database
- **SGBD**: PostgreSQL 15.0
- **Migration Tool**: Flyway
- **Connection Pooling**: HikariCP (Spring Boot default)
- **Testing**: H2 in-memory database

### API Documentation
- **Tool**: Springdoc OpenAPI 2.1.0
- **Format**: OpenAPI 3.0
- **UI**: Swagger UI included

### DevOps
- **CI/CD**: GitHub Actions workflows included
- **Containerization**: Docker and docker-compose
- **Java Distribution**: temurin
- **Maven Options**: -Xmx1024m

## Getting Started

### Prerequisites
- Java 21
- Maven 3.3.3
- Docker (optional, for local development)

### Using Templates

1. **Access Backstage UI**
   - Navigate to your Backstage instance
   - Go to "Create" section

2. **Select Template**
   - Choose from available templates
   - Review template description

3. **Configure Parameters**
   - Component ID (service name)
   - Group ID (Maven group)
   - Owner (team/user)
   - Additional options

4. **Create Service**
   - Click "Create"
   - Wait for scaffolding to complete
   - Access your new repository

### Local Development

```bash
# Clone repository
git clone <repository-url>

# Run with Maven
mvn spring-boot:run

# Run with Docker Compose
docker-compose up

# Run tests
mvn test

# Check coverage
mvn verify
```

## Configuration

### Environment Profiles

All templates include multiple environment profiles:

- `local` - Local development
- `develop` - Development environment
- `test` - Testing environment
- `staging` - Staging environment
- `prod` - Production environment

### Database Configuration

Default PostgreSQL configuration:
- **Port**: 5432
- **Database**: `<service-name>_db`
- **User**: postgres
- **Migrations**: Flyway scripts in `src/main/resources/db/migration/`

## CI/CD Pipeline

Generated projects include GitHub Actions workflows:

### Build & Test
- Runs on every push
- Executes all tests
- Generates coverage report

### Quality Gates
- Minimum 85% code coverage
- Build must pass
- Tests must pass

### Artifacts
- JAR file generation
- Docker image build
- Retention: 30 days

## Support

- **Organization**: addon-ai
- **Repository**: https://github.com/addon-ai/backstage-templates
- **Contact**: Platform Team

## License

MIT
