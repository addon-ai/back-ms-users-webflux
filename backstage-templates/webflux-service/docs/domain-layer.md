# Domain Layer

La capa de dominio contiene la lógica de negocio pura y las entidades del dominio.

## Principios

- **Sin dependencias externas**: No depende de frameworks ni librerías externas
- **Lógica de negocio**: Contiene las reglas de negocio core
- **Entidades**: Modelos de dominio con comportamiento

## Componentes

### Domain Models
Entidades que representan conceptos del negocio con su comportamiento asociado.

### Domain Ports
Interfaces que definen contratos para la comunicación con otras capas.

#### Input Ports (Use Cases)
Definen las operaciones que la aplicación puede realizar.

#### Output Ports (Repositories)
Definen las operaciones de persistencia necesarias.

## Ejemplo

```java
// Domain Model
public class User {
    private UserId id;
    private String email;
    private String name;
    
    // Business logic
    public void updateEmail(String newEmail) {
        validateEmail(newEmail);
        this.email = newEmail;
    }
}

// Output Port
public interface UserRepository {
    User save(User user);
    Optional<User> findById(UserId id);
}
```
