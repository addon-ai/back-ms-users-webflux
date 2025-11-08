# Repository Adapter Exception Handling Issue - Spring WebFlux Microservice

## 🚨 Critical Problem Summary

**Issue**: `DuplicateKeyException` is being converted to `InternalServerErrorException` in the repository adapter layer, preventing proper HTTP 409 Conflict responses.

**Root Cause**: Repository adapter's `onErrorMap` converts ALL exceptions to `InternalServerErrorException`, including constraint violations that should propagate to the service layer for proper business logic handling.

**Impact**: Users receive HTTP 500 Internal Server Error instead of HTTP 409 Conflict for duplicate data scenarios.

---

## 🔍 Technical Analysis

### 1. Exception Flow Problem

**Current Problematic Flow**:
```
1. UserService.create() calls userRepositoryPort.save()
2. UserRepositoryAdapter.save() calls r2dbcRepository.save()
3. Database throws DuplicateKeyException
4. ❌ UserRepositoryAdapter.onErrorMap() converts to InternalServerErrorException
5. ❌ UserService receives InternalServerErrorException (not DuplicateKeyException)
6. ❌ GlobalExceptionHandler returns HTTP 500 (not HTTP 409)
```

**Expected Correct Flow**:
```
1. UserService.create() calls userRepositoryPort.save()
2. UserRepositoryAdapter.save() calls r2dbcRepository.save()
3. Database throws DuplicateKeyException
4. ✅ UserRepositoryAdapter allows DuplicateKeyException to propagate
5. ✅ UserService.onErrorMap() converts to ConflictException
6. ✅ GlobalExceptionHandler returns HTTP 409 Conflict
```

### 2. Repository Adapter Implementation Issue

**File**: `UserRepositoryAdapter.java` - `save()` method

```java
// ❌ PROBLEMATIC: Converts ALL exceptions to InternalServerErrorException
@Override
public Mono<User> save(User user) {
    log.debug("Saving User: {}", user);
    return Mono.fromCallable(() -> mapper.toDbo(user))
            .flatMap(r2dbcRepository::save)
            .map(mapper::toDomain)
            .doOnError(e -> log.error("Database error while saving User: {}", e.getMessage(), e))
            .onErrorMap(e -> new InternalServerErrorException("Failed to save User", e));  // ❌ PROBLEM
}
```

**Problems**:
- `onErrorMap(e -> new InternalServerErrorException(...))` converts ALL exceptions
- `DuplicateKeyException` becomes `InternalServerErrorException`
- Service layer never receives the original constraint violation exception
- Business logic cannot differentiate between constraint violations and actual errors

### 3. Layer Responsibility Violation

**Architecture Principle Violation**:
- **Repository Layer**: Should handle technical database errors (connection issues, SQL syntax)
- **Service Layer**: Should handle business logic errors (constraint violations, validation)
- **Current Issue**: Repository layer is handling business logic errors

**Correct Responsibility Distribution**:
```
Repository Layer (UserRepositoryAdapter):
- ✅ Handle: Connection timeouts, SQL syntax errors, mapping failures
- ❌ Should NOT handle: Constraint violations, duplicate keys

Service Layer (UserService):
- ✅ Handle: Business logic errors, constraint violations, validation failures
- ✅ Convert: DuplicateKeyException → ConflictException
```

---

## ✅ Complete Solution

### 1. Fix Repository Adapter Exception Handling

**File**: `UserRepositoryAdapter.java`

```java
@Slf4j
@Component
@RequiredArgsConstructor
public class UserRepositoryAdapter implements UserRepositoryPort {

    private final JpaUserRepository r2dbcRepository;
    private final UserMapper mapper;

    /**
     * ✅ CORRECTED: Allow DuplicateKeyException to propagate for business logic handling
     */
    @Override
    public Mono<User> save(User user) {
        log.debug("Saving User: {}", user);
        return Mono.fromCallable(() -> mapper.toDbo(user))
                .flatMap(r2dbcRepository::save)
                .map(mapper::toDomain)
                .doOnError(e -> log.error("Database error while saving User: {}", e.getMessage(), e))
                .onErrorMap(ex -> {
                    // Allow DuplicateKeyException to propagate for proper handling in service layer
                    if (ex instanceof DuplicateKeyException) {
                        return ex;  // ✅ Let it propagate unchanged
                    }
                    // Convert other technical errors to InternalServerErrorException
                    return new InternalServerErrorException("Failed to save User", ex);
                });
    }
    
    // ... other methods remain unchanged ...
}
```

### 2. Add Required Import

**File**: `UserRepositoryAdapter.java` - Add import

```java
import org.springframework.dao.DuplicateKeyException;
```

### 3. Service Layer Exception Mapping (Already Implemented)

**File**: `UserService.java`

```java
@Override
public Mono<CreateUserResponseContent> create(CreateUserRequestContent request) {
    logger.info("Executing CreateUser with request: {}", request);
    
    return Mono.fromCallable(() -> userMapper.fromCreateRequest(request))
            .flatMap(userRepositoryPort::save)  // ✅ Now receives DuplicateKeyException
            .map(savedUser -> {
                logger.info("User created successfully with ID: {}", savedUser.getUserId());
                return userMapper.toCreateResponse(savedUser);
            })
            .onErrorMap(DuplicateKeyException.class, ex -> {  // ✅ Can now handle it
                String message = ex.getMessage();
                if (message.contains("users_username_key")) {
                    return new ConflictException("Username already exists");
                } else if (message.contains("users_email_key")) {
                    return new ConflictException("Email already exists");
                } else {
                    return new ConflictException("User data conflicts with existing records");
                }
            })
            .doOnError(e -> logger.error("Error in CreateUser", e, request));
}
```

### 4. Enhanced Repository Exception Handling Pattern

**Advanced Implementation with Specific Exception Types**:

```java
@Override
public Mono<User> save(User user) {
    log.debug("Saving User: {}", user);
    return Mono.fromCallable(() -> mapper.toDbo(user))
            .flatMap(r2dbcRepository::save)
            .map(mapper::toDomain)
            .doOnError(e -> log.error("Database error while saving User: {}", e.getMessage(), e))
            .onErrorMap(this::mapRepositoryException);
}

/**
 * ✅ NEW: Map repository exceptions based on type and business context
 */
private Throwable mapRepositoryException(Throwable ex) {
    // Business logic exceptions - let them propagate to service layer
    if (ex instanceof DuplicateKeyException) {
        return ex;  // Constraint violations are business logic
    }
    
    if (ex instanceof DataIntegrityViolationException) {
        return ex;  // Data integrity issues are business logic
    }
    
    // Technical exceptions - convert to infrastructure errors
    if (ex instanceof R2dbcException) {
        return new InternalServerErrorException("Database connection error", ex);
    }
    
    if (ex instanceof IllegalArgumentException) {
        return new InternalServerErrorException("Invalid database operation", ex);
    }
    
    // Default: treat as technical error
    return new InternalServerErrorException("Failed to save User", ex);
}
```

### 5. Update All Repository Methods Consistently

**Apply Same Pattern to Other Methods**:

```java
@Override
public Mono<User> findById(String id) {
    log.debug("Finding User by id: {}", id);
    return r2dbcRepository.findById(UUID.fromString(id))
            .map(mapper::toDomain)
            .doOnError(e -> log.error("Database error while finding User by id {}: {}", id, e.getMessage(), e))
            .onErrorMap(ex -> {
                // No business logic exceptions expected for findById
                return new InternalServerErrorException("Failed to find User by id", ex);
            });
}

@Override
public Flux<User> findAll() {
    log.debug("Finding all Users");
    return r2dbcRepository.findAll()
            .map(mapper::toDomain)
            .doOnError(e -> log.error("Database error while finding all Users: {}", e.getMessage(), e))
            .onErrorMap(ex -> {
                // No business logic exceptions expected for findAll
                return new InternalServerErrorException("Failed to find all Users", ex);
            });
}
```

---

## 🎯 Code Generation Guidelines

### For Python/Mustache Template Authors

1. **Repository Adapter Exception Mapping Template**:
```mustache
@Override
public Mono<{{entityName}}> save({{entityName}} {{entityName.toLowerCase}}) {
    log.debug("Saving {{entityName}}: {}", {{entityName.toLowerCase}});
    return Mono.fromCallable(() -> mapper.toDbo({{entityName.toLowerCase}}))
            .flatMap(r2dbcRepository::save)
            .map(mapper::toDomain)
            .doOnError(e -> log.error("Database error while saving {{entityName}}: {}", e.getMessage(), e))
            .onErrorMap(ex -> {
                // Allow business logic exceptions to propagate
                {{#businessExceptions}}
                if (ex instanceof {{exceptionType}}) {
                    return ex;  // Let service layer handle business logic
                }
                {{/businessExceptions}}
                // Convert technical errors
                return new InternalServerErrorException("Failed to save {{entityName}}", ex);
            });
}
```

2. **Service Layer Exception Mapping Template**:
```mustache
@Override
public Mono<Create{{entityName}}ResponseContent> create(Create{{entityName}}RequestContent request) {
    logger.info("Executing Create{{entityName}} with request: {}", request);
    
    return Mono.fromCallable(() -> {{entityName.toLowerCase}}Mapper.fromCreateRequest(request))
            .flatMap({{entityName.toLowerCase}}RepositoryPort::save)
            .map(saved{{entityName}} -> {
                logger.info("{{entityName}} created successfully with ID: {}", saved{{entityName}}.get{{entityName}}Id());
                return {{entityName.toLowerCase}}Mapper.toCreateResponse(saved{{entityName}});
            })
            {{#constraintMappings}}
            .onErrorMap({{exceptionType}}.class, ex -> {
                String message = ex.getMessage();
                {{#constraints}}
                if (message.contains("{{constraintName}}")) {
                    return new ConflictException("{{errorMessage}}");
                }
                {{/constraints}}
                return new ConflictException("{{entityName}} data conflicts with existing records");
            })
            {{/constraintMappings}}
            .doOnError(e -> logger.error("Error in Create{{entityName}}", e, request));
}
```

3. **Template Context Variables**:
```json
{
  "entityName": "User",
  "businessExceptions": [
    {"exceptionType": "DuplicateKeyException"},
    {"exceptionType": "DataIntegrityViolationException"}
  ],
  "constraintMappings": [
    {
      "exceptionType": "DuplicateKeyException",
      "constraints": [
        {
          "constraintName": "users_username_key",
          "errorMessage": "Username already exists"
        },
        {
          "constraintName": "users_email_key", 
          "errorMessage": "Email already exists"
        }
      ]
    }
  ]
}
```

### Required Imports Template

**Repository Adapter Imports**:
```mustache
import org.springframework.dao.DuplicateKeyException;
import org.springframework.dao.DataIntegrityViolationException;
import io.r2dbc.spi.R2dbcException;
```

**Service Layer Imports**:
```mustache
import com.example.{{packageName}}.infrastructure.config.exceptions.ConflictException;
import org.springframework.dao.DuplicateKeyException;
```

---

## 🧪 Testing Strategy

### Unit Tests for Repository Adapter

```java
@ExtendWith(MockitoExtension.class)
class UserRepositoryAdapterTest {
    
    @Test
    void shouldPropagateDuplicateKeyException() {
        // Given
        DuplicateKeyException dbException = new DuplicateKeyException(
            "duplicate key value violates unique constraint \"users_username_key\""
        );
        when(r2dbcRepository.save(any())).thenReturn(Mono.error(dbException));
        
        User user = User.builder().username("testuser").build();
        
        // When & Then
        StepVerifier.create(repositoryAdapter.save(user))
            .expectError(DuplicateKeyException.class)  // ✅ Should propagate unchanged
            .verify();
    }
    
    @Test
    void shouldConvertTechnicalExceptionsToInternalServerError() {
        // Given
        R2dbcException technicalException = new R2dbcException("Connection timeout");
        when(r2dbcRepository.save(any())).thenReturn(Mono.error(technicalException));
        
        User user = User.builder().username("testuser").build();
        
        // When & Then
        StepVerifier.create(repositoryAdapter.save(user))
            .expectError(InternalServerErrorException.class)  // ✅ Should convert technical errors
            .verify();
    }
}
```

### Integration Tests for Complete Flow

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class UserCreationIntegrationTest {
    
    @Test
    void shouldReturn409ForDuplicateUsername() {
        // Given: Create initial user
        CreateUserRequestContent initialUser = CreateUserRequestContent.builder()
            .username("testuser")
            .email("test@example.com")
            .build();
            
        webTestClient.post()
            .uri("/users")
            .header("X-Request-ID", "test1")
            .bodyValue(initialUser)
            .exchange()
            .expectStatus().isCreated();
            
        // When: Try to create user with same username
        CreateUserRequestContent duplicateUser = CreateUserRequestContent.builder()
            .username("testuser")  // Same username
            .email("different@example.com")
            .build();
            
        // Then: Should return 409 Conflict (not 500 Internal Server Error)
        webTestClient.post()
            .uri("/users")
            .header("X-Request-ID", "test2")
            .bodyValue(duplicateUser)
            .exchange()
            .expectStatus().isEqualTo(HttpStatus.CONFLICT)  // ✅ 409, not 500
            .expectBody()
            .jsonPath("$.status").isEqualTo(409)
            .jsonPath("$.error").isEqualTo("Conflict")
            .jsonPath("$.message").isEqualTo("Username already exists");
    }
}
```

---

## 📋 Implementation Checklist

- [x] **Repository Adapter**: Allow `DuplicateKeyException` to propagate
- [x] **Import Statements**: Add `DuplicateKeyException` import to repository adapter
- [x] **Exception Mapping**: Differentiate between business and technical exceptions
- [x] **Service Layer**: Handle `DuplicateKeyException` with `onErrorMap`
- [x] **Global Handler**: Add `DuplicateKeyException` handler as fallback
- [ ] **Unit Tests**: Test exception propagation in repository adapter
- [ ] **Integration Tests**: Test complete flow from database to HTTP response
- [ ] **Documentation**: Update architecture documentation with exception handling patterns

---

## 🎖️ Best Practices

1. **Layer Separation**: Repository handles technical errors, Service handles business errors
2. **Exception Propagation**: Let business exceptions bubble up to appropriate layer
3. **Specific Handling**: Handle specific exception types, not generic `Exception`
4. **Fallback Strategy**: Provide fallback handlers at multiple levels
5. **Consistent Patterns**: Apply same exception handling pattern across all entities
6. **Clear Logging**: Log at appropriate level (WARN for business, ERROR for technical)
7. **Testing Coverage**: Test both exception propagation and conversion scenarios

---

## 🔄 Before vs After Comparison

### Before (❌ Broken):
```
Database: DuplicateKeyException
    ↓
Repository: onErrorMap(e -> InternalServerErrorException)  ❌ CONVERTS
    ↓
Service: Receives InternalServerErrorException  ❌ WRONG TYPE
    ↓
Handler: Returns HTTP 500  ❌ WRONG STATUS
```

### After (✅ Fixed):
```
Database: DuplicateKeyException
    ↓
Repository: onErrorMap(ex -> ex instanceof DuplicateKeyException ? ex : ...)  ✅ PROPAGATES
    ↓
Service: onErrorMap(DuplicateKeyException -> ConflictException)  ✅ CONVERTS
    ↓
Handler: Returns HTTP 409  ✅ CORRECT STATUS
```

---

**Priority**: Critical - Blocking proper error handling  
**Effort**: Low - Simple exception mapping fix  
**Risk**: Very Low - Improves error handling without breaking existing functionality

---

**Author**: Senior Software Architect  
**Date**: 2024-11-08  
**Version**: 1.0.0