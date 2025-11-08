# Complete Exception Handling Solution - Spring WebFlux Code Generation

## 🚨 Problem Summary

**Issue**: Microservice returns HTTP 500 Internal Server Error instead of HTTP 409 Conflict when attempting to create users with duplicate username/email.

**Root Cause**: Multi-layer exception handling problem where `DuplicateKeyException` is incorrectly converted to `InternalServerErrorException` in the repository adapter layer, preventing proper business logic handling in the service layer.

**Impact**: Poor user experience with generic error messages and incorrect HTTP status codes violating REST API best practices.

---

## 🔍 Complete Technical Analysis

### 1. Exception Flow Problem

**Current Broken Flow**:
```
Database Layer: DuplicateKeyException (constraint violation)
    ↓
Repository Adapter: onErrorMap(ALL → InternalServerErrorException) ❌ WRONG
    ↓
Service Layer: Receives InternalServerErrorException ❌ CANNOT HANDLE PROPERLY
    ↓
Global Handler: Returns HTTP 500 ❌ WRONG STATUS CODE
```

**Expected Correct Flow**:
```
Database Layer: DuplicateKeyException (constraint violation)
    ↓
Repository Adapter: Allow DuplicateKeyException to propagate ✅ CORRECT
    ↓
Service Layer: onErrorMap(DuplicateKeyException → ConflictException) ✅ BUSINESS LOGIC
    ↓
Global Handler: Returns HTTP 409 Conflict ✅ CORRECT STATUS CODE
```

### 2. Layer Responsibility Issues

**Repository Adapter Layer** (Infrastructure):
- ❌ **Current**: Handles ALL exceptions as technical errors
- ✅ **Should**: Only handle technical database errors (connections, timeouts)
- ✅ **Should**: Allow business constraint violations to propagate

**Service Layer** (Application):
- ❌ **Current**: Cannot receive constraint violations
- ✅ **Should**: Handle business logic exceptions (duplicates, validation)
- ✅ **Should**: Convert domain exceptions to appropriate HTTP responses

### 3. Code Generation Impact

**Problem for Python/Mustache Generation**:
- Templates generate repository adapters that convert ALL exceptions
- No differentiation between technical and business exceptions
- Service layer templates cannot handle constraint violations properly
- Global exception handlers miss business-specific error scenarios

---

## ✅ Complete Solution Architecture

### 1. Repository Adapter Exception Strategy

**File**: `{{EntityName}}RepositoryAdapter.java`

```java
@Slf4j
@Component
@RequiredArgsConstructor
public class {{EntityName}}RepositoryAdapter implements {{EntityName}}RepositoryPort {

    private final Jpa{{EntityName}}Repository r2dbcRepository;
    private final {{EntityName}}Mapper mapper;

    /**
     * ✅ CORRECTED: Selective exception handling based on business context
     */
    @Override
    public Mono<{{EntityName}}> save({{EntityName}} {{entityName.toLowerCase}}) {
        log.debug("Saving {{EntityName}}: {}", {{entityName.toLowerCase}});
        return Mono.fromCallable(() -> mapper.toDbo({{entityName.toLowerCase}}))
                .flatMap(r2dbcRepository::save)
                .map(mapper::toDomain)
                .doOnError(e -> log.error("Database error while saving {{EntityName}}: {}", e.getMessage(), e))
                .onErrorMap(this::mapRepositoryException);
    }

    /**
     * ✅ NEW: Smart exception mapping based on exception type and business context
     */
    private Throwable mapRepositoryException(Throwable ex) {
        // Business logic exceptions - propagate to service layer
        if (ex instanceof DuplicateKeyException) {
            return ex;  // Constraint violations are business decisions
        }
        
        if (ex instanceof DataIntegrityViolationException) {
            return ex;  // Data integrity is business logic
        }
        
        // Technical exceptions - convert to infrastructure errors
        if (ex instanceof R2dbcException) {
            return new InternalServerErrorException("Database connection error", ex);
        }
        
        if (ex instanceof IllegalArgumentException) {
            return new InternalServerErrorException("Invalid database operation", ex);
        }
        
        // Default: treat unknown exceptions as technical errors
        return new InternalServerErrorException("Failed to save {{EntityName}}", ex);
    }
    
    // Other methods handle only technical exceptions
    @Override
    public Mono<{{EntityName}}> findById(String id) {
        log.debug("Finding {{EntityName}} by id: {}", id);
        return r2dbcRepository.findById(UUID.fromString(id))
                .map(mapper::toDomain)
                .doOnError(e -> log.error("Database error while finding {{EntityName}} by id {}: {}", id, e.getMessage(), e))
                .onErrorMap(ex -> new InternalServerErrorException("Failed to find {{EntityName}} by id", ex));
    }
}
```

### 2. Service Layer Business Exception Handling

**File**: `{{EntityName}}Service.java`

```java
@Service
@RequiredArgsConstructor
public class {{EntityName}}Service implements {{EntityName}}UseCase {

    private final {{EntityName}}RepositoryPort {{entityName.toLowerCase}}RepositoryPort;
    private final {{EntityName}}Mapper {{entityName.toLowerCase}}Mapper;

    /**
     * ✅ CORRECTED: Handle business exceptions with proper HTTP status mapping
     */
    @Override
    public Mono<Create{{EntityName}}ResponseContent> create(Create{{EntityName}}RequestContent request) {
        logger.info("Executing Create{{EntityName}} with request: {}", request);
        
        return Mono.fromCallable(() -> {{entityName.toLowerCase}}Mapper.fromCreateRequest(request))
                .flatMap({{entityName.toLowerCase}}RepositoryPort::save)
                .map(saved{{EntityName}} -> {
                    logger.info("{{EntityName}} created successfully with ID: {}", saved{{EntityName}}.get{{EntityName}}Id());
                    return {{entityName.toLowerCase}}Mapper.toCreateResponse(saved{{EntityName}});
                })
                .onErrorMap(DuplicateKeyException.class, this::mapDuplicateKeyException)
                .doOnError(e -> logger.error("Error in Create{{EntityName}}", e, request));
    }

    /**
     * ✅ NEW: Map constraint violations to specific business conflicts
     */
    private ConflictException mapDuplicateKeyException(DuplicateKeyException ex) {
        String message = ex.getMessage().toLowerCase();
        
        {{#uniqueConstraints}}
        if (message.contains("{{constraintName}}")) {
            return new ConflictException("{{errorMessage}}");
        }
        {{/uniqueConstraints}}
        
        // Generic constraint violation fallback
        return new ConflictException("{{EntityName}} data conflicts with existing records");
    }
}
```

### 3. Global Exception Handler Enhancement

**File**: `GlobalExceptionHandler.java`

```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    
    private static final LoggingUtils logger = LoggingUtils.getLogger(GlobalExceptionHandler.class);

    /**
     * ✅ Handle ConflictException from service layer (primary)
     */
    @ExceptionHandler(ConflictException.class)
    public ResponseEntity<Map<String, Object>> handleConflictException(
            ConflictException ex, WebRequest request) {
        logger.warn("Resource conflict: {}", ex.getMessage());
        
        Map<String, Object> response = new HashMap<>();
        response.put("timestamp", OffsetDateTime.now());
        response.put("status", HttpStatus.CONFLICT.value());
        response.put("error", "Conflict");
        response.put("message", ex.getMessage());
        response.put("path", request.getDescription(false).replace("uri=", ""));
        
        return ResponseEntity.status(HttpStatus.CONFLICT).body(response);
    }

    /**
     * ✅ Handle DuplicateKeyException as fallback (secondary)
     */
    @ExceptionHandler(DuplicateKeyException.class)
    public ResponseEntity<Map<String, Object>> handleDuplicateKeyException(
            DuplicateKeyException ex, WebRequest request) {
        logger.warn("Duplicate key constraint violation: {}", ex.getMessage());
        
        String message = "Resource already exists";
        {{#globalConstraintMappings}}
        if (ex.getMessage().contains("{{constraintName}}")) {
            message = "{{errorMessage}}";
        }
        {{/globalConstraintMappings}}
        
        Map<String, Object> response = new HashMap<>();
        response.put("timestamp", OffsetDateTime.now());
        response.put("status", HttpStatus.CONFLICT.value());
        response.put("error", "Conflict");
        response.put("message", message);
        response.put("path", request.getDescription(false).replace("uri=", ""));
        
        return ResponseEntity.status(HttpStatus.CONFLICT).body(response);
    }
}
```

---

## 🎯 Python/Mustache Code Generation Templates

### 1. Repository Adapter Template

**File**: `repository_adapter.mustache`

```mustache
package {{packageName}}.infrastructure.adapters.output.persistence.adapter;

import {{packageName}}.domain.ports.output.{{EntityName}}RepositoryPort;
import {{packageName}}.domain.model.{{EntityName}};
import {{packageName}}.infrastructure.adapters.output.persistence.entity.{{EntityName}}Dbo;
import {{packageName}}.infrastructure.adapters.output.persistence.repository.Jpa{{EntityName}}Repository;
import {{packageName}}.application.mapper.{{EntityName}}Mapper;
import {{packageName}}.infrastructure.config.exceptions.InternalServerErrorException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
import org.springframework.dao.DuplicateKeyException;
import org.springframework.dao.DataIntegrityViolationException;
import io.r2dbc.spi.R2dbcException;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import java.util.UUID;

/**
 * Reactive repository adapter implementing the {{EntityName}} domain port.
 */
@Slf4j
@Component
@RequiredArgsConstructor
public class {{EntityName}}RepositoryAdapter implements {{EntityName}}RepositoryPort {

    private final Jpa{{EntityName}}Repository r2dbcRepository;
    private final {{EntityName}}Mapper mapper;

    @Override
    public Mono<{{EntityName}}> save({{EntityName}} {{entityName.toLowerCase}}) {
        log.debug("Saving {{EntityName}}: {}", {{entityName.toLowerCase}});
        return Mono.fromCallable(() -> mapper.toDbo({{entityName.toLowerCase}}))
                .flatMap(r2dbcRepository::save)
                .map(mapper::toDomain)
                .doOnError(e -> log.error("Database error while saving {{EntityName}}: {}", e.getMessage(), e))
                .onErrorMap(this::mapRepositoryException);
    }

    /**
     * Smart exception mapping - business vs technical exceptions
     */
    private Throwable mapRepositoryException(Throwable ex) {
        // Business logic exceptions - let service layer handle
        {{#businessExceptions}}
        if (ex instanceof {{exceptionType}}) {
            return ex;  // Propagate for business logic handling
        }
        {{/businessExceptions}}
        
        // Technical exceptions - convert to infrastructure errors
        {{#technicalExceptions}}
        if (ex instanceof {{exceptionType}}) {
            return new InternalServerErrorException("{{errorMessage}}", ex);
        }
        {{/technicalExceptions}}
        
        // Default: treat as technical error
        return new InternalServerErrorException("Failed to save {{EntityName}}", ex);
    }

    {{#otherMethods}}
    @Override
    public {{returnType}} {{methodName}}({{#parameters}}{{paramType}} {{paramName}}{{#hasNext}}, {{/hasNext}}{{/parameters}}) {
        log.debug("{{logMessage}}", {{#parameters}}{{paramName}}{{#hasNext}}, {{/hasNext}}{{/parameters}});
        return {{repositoryCall}}
                {{#hasDomainMapping}}.map(mapper::toDomain){{/hasDomainMapping}}
                .doOnError(e -> log.error("{{errorMessage}}", e.getMessage(), e))
                .onErrorMap(ex -> new InternalServerErrorException("{{failureMessage}}", ex));
    }
    {{/otherMethods}}
}
```

### 2. Service Layer Template

**File**: `service.mustache`

```mustache
package {{packageName}}.application.service;

import {{packageName}}.domain.ports.input.{{EntityName}}UseCase;
import {{packageName}}.domain.ports.output.{{EntityName}}RepositoryPort;
import {{packageName}}.application.dto.{{entityName.toLowerCase}}.*;
import {{packageName}}.domain.model.{{EntityName}};
import {{packageName}}.application.mapper.{{EntityName}}Mapper;
import {{packageName}}.infrastructure.config.exceptions.NotFoundException;
import {{packageName}}.infrastructure.config.exceptions.ConflictException;
import {{packageName}}.utils.LoggingUtils;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.dao.DuplicateKeyException;
import reactor.core.publisher.Mono;
import reactor.core.publisher.Flux;
import java.util.List;

/**
 * Application service implementing {{EntityName}} use cases.
 */
@Service
@RequiredArgsConstructor
public class {{EntityName}}Service implements {{EntityName}}UseCase {

    private static final LoggingUtils logger = LoggingUtils.getLogger({{EntityName}}Service.class);
    
    private final {{EntityName}}RepositoryPort {{entityName.toLowerCase}}RepositoryPort;
    private final {{EntityName}}Mapper {{entityName.toLowerCase}}Mapper;

    @Override
    public Mono<Create{{EntityName}}ResponseContent> create(Create{{EntityName}}RequestContent request) {
        logger.info("Executing Create{{EntityName}} with request: {}", request);
        
        return Mono.fromCallable(() -> {{entityName.toLowerCase}}Mapper.fromCreateRequest(request))
                .flatMap({{entityName.toLowerCase}}RepositoryPort::save)
                .map(saved{{EntityName}} -> {
                    logger.info("{{EntityName}} created successfully with ID: {}", saved{{EntityName}}.get{{EntityName}}Id());
                    return {{entityName.toLowerCase}}Mapper.toCreateResponse(saved{{EntityName}});
                })
                {{#hasConstraintHandling}}
                .onErrorMap(DuplicateKeyException.class, this::mapDuplicateKeyException)
                {{/hasConstraintHandling}}
                .doOnError(e -> logger.error("Error in Create{{EntityName}}", e, request));
    }

    {{#hasConstraintHandling}}
    /**
     * Map constraint violations to specific business conflicts
     */
    private ConflictException mapDuplicateKeyException(DuplicateKeyException ex) {
        String message = ex.getMessage().toLowerCase();
        
        {{#constraintMappings}}
        if (message.contains("{{constraintName}}")) {
            return new ConflictException("{{errorMessage}}");
        }
        {{/constraintMappings}}
        
        return new ConflictException("{{EntityName}} data conflicts with existing records");
    }
    {{/hasConstraintHandling}}

    {{#otherUseCases}}
    @Override
    public {{returnType}} {{methodName}}({{#parameters}}{{paramType}} {{paramName}}{{#hasNext}}, {{/hasNext}}{{/parameters}}) {
        logger.info("Executing {{methodName}} with {{#parameters}}{{paramName}}: {}{{#hasNext}}, {{/hasNext}}{{/parameters}}", {{#parameters}}{{paramName}}{{#hasNext}}, {{/hasNext}}{{/parameters}});
        
        {{methodImplementation}}
    }
    {{/otherUseCases}}
}
```

### 3. Global Exception Handler Template

**File**: `global_exception_handler.mustache`

```mustache
package {{packageName}}.infrastructure.config.exceptions;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.dao.DuplicateKeyException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.context.request.WebRequest;
import {{packageName}}.utils.LoggingUtils;
import java.time.OffsetDateTime;
import java.util.HashMap;
import java.util.Map;

/**
 * Global exception handler for the application.
 */
@RestControllerAdvice
public class GlobalExceptionHandler {
    
    private static final LoggingUtils logger = LoggingUtils.getLogger(GlobalExceptionHandler.class);

    @ExceptionHandler(ConflictException.class)
    public ResponseEntity<Map<String, Object>> handleConflictException(
            ConflictException ex, WebRequest request) {
        logger.warn("Resource conflict: {}", ex.getMessage());
        
        Map<String, Object> response = new HashMap<>();
        response.put("timestamp", OffsetDateTime.now());
        response.put("status", HttpStatus.CONFLICT.value());
        response.put("error", "Conflict");
        response.put("message", ex.getMessage());
        response.put("path", request.getDescription(false).replace("uri=", ""));
        
        return ResponseEntity.status(HttpStatus.CONFLICT).body(response);
    }

    @ExceptionHandler(DuplicateKeyException.class)
    public ResponseEntity<Map<String, Object>> handleDuplicateKeyException(
            DuplicateKeyException ex, WebRequest request) {
        logger.warn("Duplicate key constraint violation: {}", ex.getMessage());
        
        String message = "Resource already exists";
        {{#globalConstraintMappings}}
        if (ex.getMessage().contains("{{constraintName}}")) {
            message = "{{errorMessage}}";
        }
        {{/globalConstraintMappings}}
        
        Map<String, Object> response = new HashMap<>();
        response.put("timestamp", OffsetDateTime.now());
        response.put("status", HttpStatus.CONFLICT.value());
        response.put("error", "Conflict");
        response.put("message", message);
        response.put("path", request.getDescription(false).replace("uri=", ""));
        
        return ResponseEntity.status(HttpStatus.CONFLICT).body(response);
    }

    {{#standardExceptionHandlers}}
    @ExceptionHandler({{exceptionType}}.class)
    public ResponseEntity<Map<String, Object>> handle{{exceptionName}}(
            {{exceptionType}} ex, WebRequest request) {
        logger.{{logLevel}}("{{logMessage}}: {}", ex.getMessage());
        
        Map<String, Object> response = new HashMap<>();
        response.put("timestamp", OffsetDateTime.now());
        response.put("status", HttpStatus.{{httpStatus}}.value());
        response.put("error", "{{errorType}}");
        response.put("message", {{messageExpression}});
        response.put("path", request.getDescription(false).replace("uri=", ""));
        
        return ResponseEntity.status(HttpStatus.{{httpStatus}}).body(response);
    }
    {{/standardExceptionHandlers}}
}
```

---

## 🐍 Python Code Generation Context

### Template Context Variables

```python
# context.py
def generate_entity_context(entity_config):
    return {
        "packageName": "com.example.userservice",
        "EntityName": entity_config["name"],
        "entityName": {
            "toLowerCase": entity_config["name"].lower()
        },
        
        # Repository Adapter Configuration
        "businessExceptions": [
            {"exceptionType": "DuplicateKeyException"},
            {"exceptionType": "DataIntegrityViolationException"}
        ],
        "technicalExceptions": [
            {
                "exceptionType": "R2dbcException",
                "errorMessage": "Database connection error"
            },
            {
                "exceptionType": "IllegalArgumentException", 
                "errorMessage": "Invalid database operation"
            }
        ],
        
        # Service Layer Configuration
        "hasConstraintHandling": len(entity_config.get("uniqueConstraints", [])) > 0,
        "constraintMappings": [
            {
                "constraintName": constraint["name"],
                "errorMessage": constraint["errorMessage"]
            }
            for constraint in entity_config.get("uniqueConstraints", [])
        ],
        
        # Global Handler Configuration
        "globalConstraintMappings": [
            {
                "constraintName": constraint["name"],
                "errorMessage": constraint["errorMessage"]
            }
            for constraint in entity_config.get("uniqueConstraints", [])
        ],
        
        # Standard Exception Handlers
        "standardExceptionHandlers": [
            {
                "exceptionType": "NotFoundException",
                "exceptionName": "NotFoundException", 
                "logLevel": "warn",
                "logMessage": "Resource not found",
                "httpStatus": "NOT_FOUND",
                "errorType": "Not Found",
                "messageExpression": "ex.getMessage()"
            },
            {
                "exceptionType": "MethodArgumentNotValidException",
                "exceptionName": "ValidationException",
                "logLevel": "warn", 
                "logMessage": "Validation error",
                "httpStatus": "BAD_REQUEST",
                "errorType": "Validation Failed",
                "messageExpression": "\"Invalid input data\""
            }
        ]
    }

# Entity configuration example
user_entity_config = {
    "name": "User",
    "uniqueConstraints": [
        {
            "name": "users_username_key",
            "errorMessage": "Username already exists"
        },
        {
            "name": "users_email_key",
            "errorMessage": "Email already exists"
        }
    ]
}
```

### Python Generation Script

```python
# generator.py
import json
from pathlib import Path
import pystache

class MicroserviceGenerator:
    def __init__(self, templates_dir, output_dir):
        self.templates_dir = Path(templates_dir)
        self.output_dir = Path(output_dir)
        self.renderer = pystache.Renderer()
    
    def generate_repository_adapter(self, entity_config):
        """Generate repository adapter with proper exception handling"""
        template_path = self.templates_dir / "repository_adapter.mustache"
        template_content = template_path.read_text()
        
        context = generate_entity_context(entity_config)
        
        # Add repository-specific context
        context.update({
            "otherMethods": [
                {
                    "returnType": f"Mono<{entity_config['name']}>",
                    "methodName": "findById",
                    "parameters": [{"paramType": "String", "paramName": "id"}],
                    "logMessage": f"Finding {entity_config['name']} by id: {{}}",
                    "repositoryCall": "r2dbcRepository.findById(UUID.fromString(id))",
                    "hasDomainMapping": True,
                    "errorMessage": f"Database error while finding {entity_config['name']} by id {{}}: {{}}",
                    "failureMessage": f"Failed to find {entity_config['name']} by id"
                }
                # Add other methods as needed
            ]
        })
        
        generated_code = self.renderer.render(template_content, context)
        
        output_path = self.output_dir / f"{entity_config['name']}RepositoryAdapter.java"
        output_path.write_text(generated_code)
        
        return output_path
    
    def generate_service(self, entity_config):
        """Generate service with business exception handling"""
        template_path = self.templates_dir / "service.mustache"
        template_content = template_path.read_text()
        
        context = generate_entity_context(entity_config)
        
        generated_code = self.renderer.render(template_content, context)
        
        output_path = self.output_dir / f"{entity_config['name']}Service.java"
        output_path.write_text(generated_code)
        
        return output_path
    
    def generate_exception_handler(self, entities_config):
        """Generate global exception handler for all entities"""
        template_path = self.templates_dir / "global_exception_handler.mustache"
        template_content = template_path.read_text()
        
        # Collect all unique constraints from all entities
        all_constraints = []
        for entity_config in entities_config:
            all_constraints.extend(entity_config.get("uniqueConstraints", []))
        
        context = {
            "packageName": "com.example.userservice",
            "globalConstraintMappings": [
                {
                    "constraintName": constraint["name"],
                    "errorMessage": constraint["errorMessage"]
                }
                for constraint in all_constraints
            ],
            "standardExceptionHandlers": [
                # Standard handlers as defined above
            ]
        }
        
        generated_code = self.renderer.render(template_content, context)
        
        output_path = self.output_dir / "GlobalExceptionHandler.java"
        output_path.write_text(generated_code)
        
        return output_path

# Usage example
if __name__ == "__main__":
    generator = MicroserviceGenerator("templates/", "output/")
    
    entities = [user_entity_config]  # Add more entities as needed
    
    for entity in entities:
        generator.generate_repository_adapter(entity)
        generator.generate_service(entity)
    
    generator.generate_exception_handler(entities)
```

---

## 📋 Implementation Checklist for Code Generation

### Repository Adapter Generation
- [ ] **Exception Type Detection**: Identify business vs technical exceptions
- [ ] **Selective Propagation**: Allow constraint violations to bubble up
- [ ] **Technical Error Conversion**: Convert connection/syntax errors to InternalServerErrorException
- [ ] **Logging Strategy**: Log business exceptions at WARN, technical at ERROR

### Service Layer Generation  
- [ ] **Constraint Mapping**: Map specific constraint names to user-friendly messages
- [ ] **Business Logic Handling**: Convert DuplicateKeyException to ConflictException
- [ ] **Error Context**: Include entity-specific information in error messages
- [ ] **Fallback Handling**: Generic conflict message for unknown constraints

### Global Handler Generation
- [ ] **Primary Handlers**: Handle ConflictException from service layer
- [ ] **Fallback Handlers**: Handle DuplicateKeyException that bypassed service layer
- [ ] **Consistent Response Format**: Maintain same error response structure
- [ ] **HTTP Status Mapping**: Correct status codes for different exception types

### Template Configuration
- [ ] **Entity Metadata**: Extract unique constraints from entity definitions
- [ ] **Constraint Naming**: Map database constraint names to business messages
- [ ] **Package Structure**: Generate correct import statements and package declarations
- [ ] **Method Generation**: Create appropriate CRUD methods with exception handling

---

## 🎖️ Best Practices for Code Generation

1. **Layer Separation**: Repository handles technical, Service handles business
2. **Exception Propagation**: Let business exceptions bubble up to appropriate layer
3. **Specific Handling**: Handle specific exception types, not generic Exception
4. **Consistent Patterns**: Apply same exception handling pattern across all entities
5. **Template Reusability**: Create generic templates that work for any entity
6. **Configuration Driven**: Use entity metadata to drive exception handling logic
7. **Fallback Strategy**: Provide multiple levels of exception handling
8. **Testing Integration**: Generate test cases that verify exception handling flows

---

**Priority**: Critical - Foundation for proper error handling across all generated code  
**Effort**: Medium - Requires template updates and generation logic changes  
**Risk**: Low - Improves error handling without breaking existing functionality

---

**Author**: Senior Software Architect  
**Date**: 2024-11-08  
**Version**: 1.0.0