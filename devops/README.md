# 🎭 Backstage Template - Spring WebFlux Microservice

Este directorio contiene el **Software Template** de Backstage para generar microservicios reactivos con Spring WebFlux y arquitectura hexagonal.

## 📁 Estructura

```
devops/
├── template.yaml           # Definición del template de Backstage
├── skeleton/               # Plantillas Mustache del proyecto
│   ├── catalog-info.yaml  # Descriptor del componente (plantilla)
│   ├── src/               # Código fuente (plantillas)
│   ├── pom.xml            # Maven POM (plantilla)
│   └── ...                # Otros archivos del proyecto
└── README.md              # Este archivo
```

## 🎯 Archivos Principales

### 1. `template.yaml`
**Propósito:** Define el Software Template en Backstage

**Contiene:**
- 📝 Formularios interactivos (parameters)
- 🔄 Pasos de scaffolding (steps)
- 📦 Configuración de publicación
- 🔗 Outputs y links

**Uso:** Se registra en Backstage para crear nuevos proyectos

### 2. `skeleton/catalog-info.yaml`
**Propósito:** Plantilla del descriptor del componente

**Contiene:**
- Variables Mustache: `${{ values.component_id }}`
- Metadata del componente
- Anotaciones de integración
- Relaciones con otros componentes

**Uso:** Se procesa durante el scaffolding y se genera en el nuevo repo

## 🚀 Cómo Usar

### Registrar el Template en Backstage

1. **Opción 1: Via UI**
   ```
   Backstage → Create → Register Existing Component
   URL: https://github.com/your-org/your-repo/blob/main/devops/template.yaml
   ```

2. **Opción 2: Via catalog-info.yaml**
   ```yaml
   apiVersion: backstage.io/v1alpha1
   kind: Location
   metadata:
     name: templates
   spec:
     type: url
     targets:
       - https://github.com/your-org/your-repo/blob/main/devops/template.yaml
   ```

### Crear un Nuevo Proyecto

1. Ir a **Create** en Backstage
2. Seleccionar **"Reactive microservice for users management with Spring WebFlux"**
3. Llenar el formulario con:
   - Información del componente
   - Configuración Java
   - Entidades del dominio
   - Configuración de base de datos
   - Características adicionales
4. Click en **Create**
5. Backstage generará el proyecto y lo publicará en GitHub

## 🔧 Variables Disponibles

Las siguientes variables están disponibles en las plantillas Mustache:

### Información del Componente
- `values.component_id` - ID del componente
- `values.description` - Descripción
- `values.owner` - Propietario (equipo)
- `values.system` - Sistema padre
- `values.lifecycle` - Ciclo de vida
- `values.tags` - Array de etiquetas

### Configuración Java
- `values.groupId` - Maven Group ID
- `values.artifactId` - Maven Artifact ID
- `values.javaVersion` - Versión de Java
- `values.springBootVersion` - Versión de Spring Boot
- `values.java_package_path` - Ruta del paquete Java
- `values.java_package_name` - Nombre del paquete Java

### Arquitectura Hexagonal
- `values.entities` - Array de entidades del dominio
- `values.useCases` - Array de casos de uso
- `values.repositories` - Array de repositorios

### Base de Datos
- `values.database` - Motor de BD (PostgreSQL, MySQL, H2)
- `values.enableLiquibase` - Boolean
- `values.enableR2DBC` - Boolean

### Características
- `values.enableSwagger` - Boolean
- `values.enableActuator` - Boolean
- `values.enableSecurity` - Boolean
- `values.coverageThreshold` - Number (0-100)

### CI/CD
- `values.enableGithubActions` - Boolean
- `values.enableDocker` - Boolean
- `values.environments` - Array de ambientes

### Valores Computados
- `values.application_name` - Nombre de la aplicación
- `values.database_name` - Nombre de la BD
- `values.port` - Puerto (8080)

### Destino
- `values.destination.owner` - Owner del repo GitHub
- `values.destination.repo` - Nombre del repo

## 📝 Sintaxis Mustache

### Variables Simples
```yaml
name: ${{ values.component_id }}
```

### Condicionales
```yaml
{{#if values.enableSwagger}}
springdoc.enabled=true
{{/if}}
```

### Loops
```yaml
{{#each values.entities}}
- ${{ this.name }}
{{/each}}
```

### Defaults
```yaml
lifecycle: ${{ values.lifecycle | default("experimental") }}
```

## ⚠️ Notas Importantes

1. **No editar `catalog-info.yaml` directamente en `devops/`**
   - Debe estar en `devops/skeleton/`
   - Es una plantilla, no un archivo final

2. **Variables Mustache**
   - Usar `${{ values.x }}` para variables
   - Usar `{{#if}}`, `{{#each}}` para lógica
   - Backstage procesa estas variables durante el scaffolding

3. **Validación**
   - `template.yaml` se valida al registrarlo en Backstage
   - `skeleton/catalog-info.yaml` se valida después de procesarse

4. **Testing**
   - Probar el template creando un proyecto de prueba
   - Verificar que todas las variables se reemplacen correctamente

## 🔗 Referencias

- [Backstage Software Templates](https://backstage.io/docs/features/software-templates/)
- [Template Syntax](https://backstage.io/docs/features/software-templates/writing-templates)
- [Catalog Format](https://backstage.io/docs/features/software-catalog/descriptor-format)
- [Built-in Actions](https://backstage.io/docs/features/software-templates/builtin-actions)

## 📧 Soporte

Para preguntas o problemas con el template:
- Crear un issue en el repositorio
- Contactar al equipo de plataforma
