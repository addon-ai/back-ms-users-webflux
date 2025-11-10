# Infrastructure Layer

La capa de infraestructura contiene los adaptadores que conectan con el mundo exterior.

## Responsabilidades

- **Input Adapters**: REST Controllers, GraphQL, etc.
- **Output Adapters**: Persistencia, APIs externas, etc.
- **Configuración**: Beans de Spring, configuraciones

## Componentes

### Input Adapters (REST Controllers)
Exponen endpoints HTTP y delegan a los servicios de aplicación.

### Output Adapters (Persistence)
Implementan los output ports usando JPA/R2DBC.

### Configuration
Configuración de Spring Boot, beans, etc.

## Ejemplo

```java
// Input Adapter (REST Controller)
@RestController
@RequestMapping("/api/users")
public class UserController {
    private final CreateUserUseCase createUserUseCase;
    
    @PostMapping
    public ResponseEntity<UserResponse> createUser(@RequestBody CreateUserRequest request) {
        UserResponse response = createUserUseCase.createUser(request);
        return ResponseEntity.ok(response);
    }
}

// Output Adapter (JPA Repository)
@Repository
public class UserRepositoryAdapter implements UserRepository {
    private final UserJpaRepository jpaRepository;
    private final UserEntityMapper entityMapper;
    
    @Override
    public User save(User user) {
        UserEntity entity = entityMapper.toEntity(user);
        UserEntity saved = jpaRepository.save(entity);
        return entityMapper.toDomain(saved);
    }
}

// JPA Entity
@Entity
@Table(name = "users")
public class UserEntity {
    @Id
    private UUID id;
    private String email;
    private String name;
}
```
