# Spring Boot Service Template

Template para crear microservicios Java con Spring Boot y Arquitectura Hexagonal.

## Características

- **Java:** 21
- **Spring Boot:** 3.2.5
- **Arquitectura:** Hexagonal (Ports and Adapters)
- **Build Tool:** Maven
- **Base de Datos:** JPA con PostgreSQL/MySQL/H2

## Estructura del Proyecto

```
src/main/java/com/example/userservice/
├── application/          # Capa de Aplicación
│   ├── dto/             # Data Transfer Objects
│   ├── mapper/          # Mappers
│   └── service/         # Servicios de aplicación
├── domain/              # Capa de Dominio
│   ├── model/           # Entidades de dominio
│   └── ports/           # Puertos (interfaces)
│       ├── input/       # Puertos de entrada
│       └── output/      # Puertos de salida
├── infrastructure/      # Capa de Infraestructura
│   ├── adapters/        # Adaptadores
│   │   ├── input/rest/  # Controladores REST
│   │   └── output/persistence/ # Persistencia
│   └── config/          # Configuración
└── utils/               # Utilidades
```

## Uso

1. Selecciona este template en Backstage
2. Completa los parámetros requeridos
3. El template generará la estructura completa del proyecto
4. Ejecuta `mvn spring-boot:run` para iniciar

## Capas de la Arquitectura

- [Domain Layer](domain-layer.md) - Lógica de negocio
- [Application Layer](application-layer.md) - Casos de uso
- [Infrastructure Layer](infrastructure-layer.md) - Adaptadores
