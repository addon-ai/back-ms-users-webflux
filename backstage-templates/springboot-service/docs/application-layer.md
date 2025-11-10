# Application Layer

La capa de aplicación orquesta los casos de uso y coordina el flujo de datos.

## Responsabilidades

- **Casos de Uso**: Implementa los use cases del sistema
- **DTOs**: Define objetos de transferencia de datos
- **Mappers**: Transforma entre DTOs y entidades de dominio
- **Servicios**: Coordina la lógica de aplicación

## Componentes

### Application Services
Implementan los input ports definidos en el dominio.

### DTOs (Data Transfer Objects)
Objetos para transferir datos entre capas.

### Mappers
Transforman DTOs a entidades de dominio y viceversa (usando MapStruct).

## Ejemplo

```java
// Application Service
@Service
public class UserService implements CreateUserUseCase {
    private final UserRepository userRepository;
    private final UserMapper userMapper;
    
    @Override
    public UserResponse createUser(CreateUserRequest request) {
        User user = userMapper.toDomain(request);
        User savedUser = userRepository.save(user);
        return userMapper.toResponse(savedUser);
    }
}

// DTO
public record CreateUserRequest(
    String email,
    String name
) {}

// Mapper
@Mapper(componentModel = "spring")
public interface UserMapper {
    User toDomain(CreateUserRequest request);
    UserResponse toResponse(User user);
}
```
