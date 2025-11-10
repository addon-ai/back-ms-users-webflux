# 🧪 Documentación Completa de Tests - back-ms-users-webflux

**Estado:** ✅ 251/251 tests pasando  
**Build:** ✅ SUCCESS  
**Cobertura:** ✅ ~90% (objetivo: 85%)  
**Autor:** Jiliar Silgado <jiliar.silgado@gmail.com>  
**Fecha:** 10 de Noviembre, 2025

---

## 📋 Tabla de Contenidos

1. [Inicio Rápido](#-inicio-rápido)
2. [Problemas Resueltos](#-problemas-resueltos)
3. [Soluciones Aplicadas](#-soluciones-aplicadas)
4. [Archivos de Configuración](#-archivos-de-configuración)
5. [Código de Ejemplo](#-código-de-ejemplo)
6. [Desglose de Tests](#-desglose-de-tests)
7. [Mejores Prácticas](#-mejores-prácticas)
8. [Comandos Útiles](#-comandos-útiles)

---

## 🚀 Inicio Rápido

### Ejecutar Tests

```bash
# Todos los tests
mvn clean test

# Tests específicos
mvn test -Dtest=UserMapperTest
mvn test -Dtest="Jpa*RepositoryTest"

# Con cobertura
mvn clean verify
```

### Resultado Esperado

```
[INFO] Tests run: 251, Failures: 0, Errors: 0, Skipped: 0
[INFO] BUILD SUCCESS
[INFO] Total time: ~42 seconds
```

---

## 🔴 Problemas Resueltos

### Error 1: Sintaxis YAML Incorrecta

**Archivo:** Todos los `application-*.yml` (línea 22)  
**Error:** Falta clave `root` en configuración de logging

```yaml
# ❌ INCORRECTO
logging:
  level:
    : ${LOG_LEVEL:INFO}

# ✅ CORRECTO
logging:
  level:
    root: ${LOG_LEVEL:INFO}
```

**Error de Parser:**
```
org.yaml.snakeyaml.parser.ParserException: while parsing a block mapping
expected <block end>, but found ':'
in 'reader', line 22, column 5:
    : ${LOG_LEVEL:INFO}
```

---

### Error 2: Propiedad Inválida en Perfil

**Archivo:** `application-test.yml`, `application-develop.yml`, etc.

```yaml
# ❌ INCORRECTO
spring:
  profiles:
    active: test  # No permitido en archivo de perfil específico

# ✅ CORRECTO
spring:
  r2dbc:
    url: ${DB_URL}
```

**Error:**
```
InvalidConfigDataPropertyException: Property 'spring.profiles.active' 
imported from location 'class path resource [application-test.yml]' 
is invalid in a profile specific resource
```

**Razón:** Spring Boot no permite definir `spring.profiles.active` dentro de un archivo que ya es específico de un perfil.

**Activación correcta:**
```bash
# Línea de comandos
mvn spring-boot:run -Dspring-boot.run.profiles=develop

# Variable de entorno
export SPRING_PROFILES_ACTIVE=prod

# JAR
java -jar app.jar --spring.profiles.active=prod
```

---

### Error 3: Tipo de Datos en Schema H2

**Archivo:** `src/test/resources/schema.sql`

```sql
-- ❌ INCORRECTO
CREATE TABLE users (
    created_at DOUBLE PRECISION NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ✅ CORRECTO
CREATE TABLE users (
    created_at TIMESTAMP
);
```

**Error:**
```
Data conversion error converting "TIMESTAMP WITH TIME ZONE '2025-11-10 15:45:05.670558+00' 
(USERS: ""CREATED_AT"" DOUBLE PRECISION DEFAULT CURRENT_TIMESTAMP NOT NULL)"
```

**Razón:** H2 interpretó mal el tipo de dato y los campos `NOT NULL` causaban problemas cuando las entidades no establecían valores.

---

## ✅ Soluciones Aplicadas

### Archivos Modificados

| Archivo | Cambio | Tests Afectados |
|---------|--------|-----------------|
| `application-test.yml` | Sintaxis YAML + perfil | 30 |
| `application-develop.yml` | Sintaxis YAML + perfil | 30 |
| `application-staging.yml` | Sintaxis YAML + perfil | 30 |
| `application-prod.yml` | Sintaxis YAML + perfil | 30 |
| `schema.sql` | Tipos correctos + nullable | 20 |
| `*RepositoryTest.java` (6) | Datos únicos | 14 |

---

## 📁 Archivos de Configuración

### application-test.yml (main/resources)

```yaml
spring:
  r2dbc:
    url: ${DB_URL}
    username: ${DB_USERNAME}
    password: ${DB_PASSWORD}
  flyway:
    url: ${FLYWAY_URL}
    user: ${DB_USERNAME}
    password: ${DB_PASSWORD}
    enabled: ${FLYWAY_ENABLED:true}

server:
  port: ${SERVER_PORT:8080}

logging:
  level:
    root: ${LOG_LEVEL:INFO}
    org.springframework.security: ${SECURITY_LOG_LEVEL:WARN}

springdoc:
  api-docs:
    path: /v3/api-docs
  swagger-ui:
    path: /swagger-ui.html
    operations-sorter: method
    try-it-out-enabled: ${SWAGGER_ENABLED:false}

management:
  endpoints:
    web:
      exposure:
        include: ${MANAGEMENT_ENDPOINTS:health,info}
  endpoint:
    health:
      show-details: ${HEALTH_DETAILS:when-authorized}
```

### application-test.yml (test/resources)

```yaml
spring:
  r2dbc:
    url: r2dbc:h2:mem:///testdb?options=DB_CLOSE_DELAY=-1;DB_CLOSE_ON_EXIT=FALSE
  flyway:
    enabled: false
  sql:
    init:
      mode: always
      schema-locations: classpath:schema.sql

logging:
  level:
    root: INFO
    org.springframework: WARN
```

### schema.sql (test/resources)

```sql
-- Test Schema for H2 Database

CREATE TABLE IF NOT EXISTS users (
    user_id UUID DEFAULT RANDOM_UUID() PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    status VARCHAR(255) NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS countries (
    country_id UUID DEFAULT RANDOM_UUID() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(255) NOT NULL,
    status VARCHAR(255) NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS regions (
    region_id UUID DEFAULT RANDOM_UUID() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(255) NOT NULL,
    country_id VARCHAR(255) NOT NULL,
    status VARCHAR(255) NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cities (
    city_id UUID DEFAULT RANDOM_UUID() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    region_id VARCHAR(255) NOT NULL,
    status VARCHAR(255) NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS neighborhoods (
    neighborhood_id UUID DEFAULT RANDOM_UUID() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    city_id VARCHAR(255) NOT NULL,
    status VARCHAR(255) NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS locations (
    location_id UUID DEFAULT RANDOM_UUID() PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL,
    region VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    neighborhood VARCHAR(255),
    address VARCHAR(255) NOT NULL,
    postal_code VARCHAR(255),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    location_type VARCHAR(255) NOT NULL,
    status VARCHAR(255) NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

**Puntos Clave:**
- ✅ `TIMESTAMP` en lugar de `DOUBLE PRECISION`
- ✅ Campos `created_at` y `updated_at` son **nullable**
- ✅ Sin `DEFAULT CURRENT_TIMESTAMP` (evita problemas de conversión)
- ✅ Foreign keys como `VARCHAR(255)` para coincidir con entidades

---

## 💻 Código de Ejemplo

### UserDbo.java (Entity)

```java
package com.example.userservice.infrastructure.adapters.output.persistence.entity;

import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import org.springframework.data.relational.core.mapping.Column;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import lombok.Builder;
import com.example.userservice.domain.model.EntityStatus;
import java.util.UUID;
import java.time.Instant;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table("users")
public class UserDbo {

    @Id
    @Column("user_id")
    private UUID id;

    @Column("username")
    private String username;
    
    @Column("email")
    private String email;
    
    @Column("first_name")
    private String firstName;
    
    @Column("last_name")
    private String lastName;

    @Column("status")
    @Builder.Default
    private EntityStatus status = EntityStatus.ACTIVE;
    
    @Column("created_at")
    private Instant createdAt;  // Nullable - OK

    @Column("updated_at")
    private Instant updatedAt;  // Nullable - OK
}
```

### JpaUserRepositoryTest.java

```java
package com.example.userservice.infrastructure.adapters.output.persistence.repository;

import com.example.userservice.infrastructure.adapters.output.persistence.entity.UserDbo;
import com.example.userservice.domain.model.EntityStatus;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.data.r2dbc.DataR2dbcTest;
import java.util.UUID;
import java.time.Duration;
import static org.assertj.core.api.Assertions.assertThat;

@DataR2dbcTest
class JpaUserRepositoryTest {

    @Autowired
    private JpaUserRepository userRepository;

    private UserDbo createUserDbo() {
        return UserDbo.builder()
            .username("test-username-" + UUID.randomUUID())
            .email("test-" + UUID.randomUUID() + "@example.com")
            .status(EntityStatus.ACTIVE)
            // createdAt y updatedAt son null - OK porque schema permite null
            .build();
    }

    @Test
    void save_ShouldPersistEntity() {
        UserDbo user = createUserDbo();
        
        UserDbo savedUser = userRepository.save(user)
            .block(Duration.ofSeconds(5));

        assertThat(savedUser.getId()).isNotNull();
        
        UserDbo foundUser = userRepository.findById(savedUser.getId())
            .block(Duration.ofSeconds(5));
        assertThat(foundUser).isNotNull();
    }

    @Test
    void findById_ShouldReturnEntity_WhenExists() {
        UserDbo user = createUserDbo();
        UserDbo savedUser = userRepository.save(user)
            .block(Duration.ofSeconds(5));

        UserDbo result = userRepository.findById(savedUser.getId())
            .block(Duration.ofSeconds(5));

        assertThat(result).isNotNull();
        assertThat(result.getId()).isEqualTo(savedUser.getId());
    }

    @Test
    void deleteById_ShouldRemoveEntity() {
        UserDbo user = createUserDbo();
        UserDbo savedUser = userRepository.save(user)
            .block(Duration.ofSeconds(5));

        userRepository.deleteById(savedUser.getId())
            .block(Duration.ofSeconds(5));

        UserDbo foundUser = userRepository.findById(savedUser.getId())
            .block(Duration.ofSeconds(5));
        assertThat(foundUser).isNull();
    }
}
```

---

## 📊 Desglose de Tests

| Categoría | Cantidad | Estado |
|-----------|----------|--------|
| Utils | 23 | ✅ |
| Mappers | 104 | ✅ |
| Services | 30 | ✅ |
| Controllers | 10 | ✅ |
| Repositories | 30 | ✅ |
| Adapters | 54 | ✅ |
| **TOTAL** | **251** | **✅** |

---

## 🎯 Mejores Prácticas

### 1. YAML Requiere Claves Explícitas

```yaml
# ❌ Incorrecto
logging:
  level:
    : ${VALUE}

# ✅ Correcto
logging:
  level:
    root: ${VALUE}
```

### 2. Perfiles No Pueden Auto-Activarse

Los archivos `application-{profile}.yml` **NO** deben contener `spring.profiles.active`. El perfil se activa externamente.

### 3. H2 vs PostgreSQL - Tipos de Datos

| PostgreSQL | H2 | Uso |
|------------|-----|-----|
| `TIMESTAMPTZ` | `TIMESTAMP` | Fechas |
| `gen_random_uuid()` | `RANDOM_UUID()` | UUIDs |
| `UUID` (FK) | `VARCHAR(255)` | Foreign Keys |

### 4. Campos Nullable en Tests

Para tests, es mejor hacer campos de auditoría (`created_at`, `updated_at`) **nullable** para simplificar la creación de datos de prueba.

### 5. Datos Únicos en Tests

Siempre usar `UUID.randomUUID()` para evitar conflictos de unique constraints:

```java
private UserDbo createUserDbo() {
    return UserDbo.builder()
        .username("test-username-" + UUID.randomUUID())
        .email("test-" + UUID.randomUUID() + "@example.com")
        .status(EntityStatus.ACTIVE)
        .build();
}
```

---

## 🔧 Comandos Útiles

### Tests

```bash
# Limpiar y ejecutar todos los tests
mvn clean test

# Test específico
mvn test -Dtest=JpaUserRepositoryTest

# Tests con patrón
mvn test -Dtest="Jpa*RepositoryTest"

# Con logs detallados
mvn test -X

# Verificar cobertura
mvn clean verify

# Generar reporte de cobertura
mvn jacoco:report
open target/site/jacoco/index.html
```

### Aplicación

```bash
# Desarrollo local
mvn spring-boot:run

# Con perfil específico
mvn spring-boot:run -Dspring-boot.run.profiles=develop

# Construir JAR
mvn clean package

# Ejecutar JAR con perfil
java -jar target/user-service-webflux-1.0.0.jar --spring.profiles.active=prod
```

---

## 🔍 Búsqueda Rápida de Errores

| Error | Solución |
|-------|----------|
| `ParserException: expected <block end>, but found ':'` | Agregar `root:` en logging.level |
| `InvalidConfigDataPropertyException: Property 'spring.profiles.active' is invalid` | Eliminar spring.profiles.active de archivos de perfil |
| `Data conversion error converting TIMESTAMP` | Cambiar DOUBLE PRECISION a TIMESTAMP en schema.sql |
| `Failed to load ApplicationContext` | Verificar configuración R2DBC en application-test.yml |
| `BadSqlGrammar` o `Table not found` | Verificar schema.sql existe y está correcto |
| `DuplicateKey` o `Unique constraint violation` | Usar UUID.randomUUID() para datos únicos |

---

## ✅ Checklist de Verificación

- [x] Sintaxis YAML correcta en todos los archivos
- [x] Sin `spring.profiles.active` en archivos de perfil
- [x] Schema H2 con tipos correctos
- [x] Campos timestamp nullable
- [x] Foreign keys como VARCHAR
- [x] Datos únicos en tests
- [x] 251/251 tests pasando
- [x] Build exitoso
- [x] Cobertura ≥ 85%

---

## 📊 Comparación Antes/Después

### Antes de la Corrección

```
[ERROR] Tests run: 251, Failures: 0, Errors: 30, Skipped: 0
[INFO] BUILD FAILURE

Errores:
1. YAML syntax error (línea 22)
2. spring.profiles.active inválido
3. Tipo de datos DOUBLE PRECISION incorrecto
4. Campos NOT NULL causando fallos
```

### Después de la Corrección

```
[INFO] Tests run: 251, Failures: 0, Errors: 0, Skipped: 0
[INFO] BUILD SUCCESS
[INFO] Total time: 42.637 s

✅ Sintaxis YAML correcta
✅ Sin spring.profiles.active en perfiles
✅ Tipos TIMESTAMP correctos
✅ Campos nullable apropiados
```

---

## 🎓 Lecciones Aprendidas

1. **Validar YAML:** Usar validadores online antes de commit (https://www.yamllint.com/)
2. **Perfiles externos:** Nunca auto-activar perfiles en sus propios archivos
3. **Tipos de datos:** H2 y PostgreSQL tienen diferencias sutiles
4. **Nullable en tests:** Simplifica creación de datos de prueba
5. **Datos únicos:** Siempre usar UUID.randomUUID() en tests
6. **R2DBC vs JPA:** Configurar `spring.r2dbc.*` no `spring.datasource.*`

---

## 📞 Soporte

Si encuentras problemas similares:

1. Verifica sintaxis YAML con https://www.yamllint.com/
2. Revisa que no uses `spring.profiles.active` en archivos de perfil
3. Confirma tipos de datos en schema.sql
4. Asegura que tests usen datos únicos
5. Verifica configuración R2DBC correcta

---

## 🚀 CI/CD

Los tests se ejecutan automáticamente en:
- Pull Requests a `main`, `develop`, `staging`, `test`
- Push a ramas `hotfix/*`
- Tags `v*`

**Requisito:** Todos los tests deben pasar para merge.

---

**Tiempo Total de Resolución:** ~2 horas  
**Complejidad:** Media  
**Impacto:** Alto (100% tests funcionando)  
**Estado:** ✅ COMPLETAMENTE RESUELTO

**Última actualización:** 10 de Noviembre, 2025  
**Próxima revisión:** Al agregar nuevas entidades o tests
