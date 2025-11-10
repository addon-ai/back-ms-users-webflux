# Backstage Golden Path Generator

Convierte proyectos Java generados en **Software Templates de Backstage** (Golden Paths) listos para usar.

## 🎯 Propósito

Esta librería toma proyectos Java ya generados (Spring Boot o WebFlux con arquitectura hexagonal) y los transforma en plantillas de Backstage Scaffolder, permitiendo a los desarrolladores crear nuevos servicios desde una interfaz web.

## 🔄 Flujo de Datos

```
Proyecto Java Generado → py-backstage-goldenpath-gen → Golden Path de Backstage
```

**Entrada:** Proyecto Java en `projects/mi-servicio-webflux/`  
**Salida:** Template de Backstage en `backstage-templates/webflux-service/`

## 📁 Estructura de Salida

```
backstage-templates/
├── webflux-service/
│   ├── template.yaml          # Manifiesto de Backstage
│   └── skeleton/               # Proyecto Java "re-parametrizado"
│       ├── catalog-info.yaml   # Metadata del componente
│       ├── pom.xml             # Con variables ${{ values.component_id }}
│       └── src/
│           └── main/java/
│               └── ${{ values.java_package_path }}/  # Paquetes parametrizados
└── springboot-service/
    └── ...
```

## 🚀 Uso

### Desde el Pipeline (Automático)

El pipeline `scripts/code-gen-pipeline.sh` ejecuta automáticamente este generador:

```bash
./scripts/code-gen-pipeline.sh
```

### Uso Manual

```bash
python3 libs/py-backstage-goldenpath-gen/main.py \
    libs/config/params.json \
    projects/ \
    backstage-templates/
```

**Argumentos:**
1. `config_path` - Ruta al archivo de configuración JSON
2. `projects_dir` - Directorio con proyectos Java generados
3. `output_dir` - Directorio de salida para Golden Paths

## 🔧 Proceso de Transformación

### 1. Copia del Skeleton

Copia el proyecto Java completo a `skeleton/`:

```
projects/back-ms-users-webflux/ → backstage-templates/webflux-service/skeleton/
```

### 2. Re-Parametrización

Reemplaza valores hardcodeados por variables de Backstage:

**Antes (hardcoded):**
```xml
<artifactId>back-ms-users-webflux</artifactId>
<groupId>com.example.userservice</groupId>
```

**Después (parametrizado):**
```xml
<artifactId>${{ values.component_id }}</artifactId>
<groupId>${{ values.groupId }}</groupId>
```

**Antes (hardcoded):**
```java
package com.example.userservice.domain;
```

**Después (parametrizado):**
```java
package ${{ values.java_package_name }}.domain;
```

### 3. Renombrado de Directorios

**Antes:**
```
src/main/java/com/example/userservice/
```

**Después:**
```
src/main/java/${{ values.java_package_path }}/
```

### 4. Generación de Manifiestos

Crea `template.yaml` con:
- **Parameters:** Variables que el usuario completará (component_id, groupId, owner, etc.)
- **Steps:** Acciones de Backstage (fetch:template, publish:github, catalog:register)
- **Output:** Links al repositorio y catálogo

## 📋 Variables de Template

Las siguientes variables están disponibles en el skeleton:

| Variable | Ejemplo | Descripción |
|----------|---------|-------------|
| `values.component_id` | `user-service` | Nombre del componente |
| `values.groupId` | `com.example` | Group ID de Maven |
| `values.description` | `User management service` | Descripción del servicio |
| `values.owner` | `platform-team` | Equipo propietario |
| `values.javaVersion` | `21` | Versión de Java |
| `values.java_package_name` | `com.example.userservice` | Nombre completo del paquete |
| `values.java_package_path` | `com/example/userservice` | Ruta del paquete |

## 🎨 Personalización

### Modificar el Template

Edita `templates/template.yaml.mustache` para:
- Agregar nuevos parámetros
- Cambiar steps de Backstage
- Modificar metadata

### Agregar Nuevos Reemplazos

En `main.py`, método `_reparametrize_skeleton()`:

```python
replacements = {
    'valor_antiguo': 'valor_nuevo_con_${{ values.variable }}',
    # Agregar más reemplazos aquí
}
```

## 🔗 Integración con Backstage

### 1. Registrar el Template

En tu instancia de Backstage, registra el template:

```yaml
# app-config.yaml
catalog:
  locations:
    - type: file
      target: /path/to/backstage-templates/webflux-service/template.yaml
```

O usa el UI de Backstage:
1. Ir a "Create" → "Register Existing Component"
2. Ingresar la URL del `template.yaml`

### 2. Usar el Template

1. Ir a "Create" en Backstage
2. Seleccionar "Java WebFlux Service" (o Spring Boot)
3. Completar el formulario
4. Backstage generará el proyecto y lo publicará en GitHub

## 📦 Dependencias

- Python 3.6+
- pystache (para renderizar templates Mustache)

```bash
pip3 install pystache
```

## 🧪 Testing

Verificar que el Golden Path se generó correctamente:

```bash
# Verificar estructura
ls -la backstage-templates/webflux-service/

# Verificar que las variables fueron reemplazadas
grep -r "values.component_id" backstage-templates/webflux-service/skeleton/

# Verificar template.yaml
cat backstage-templates/webflux-service/template.yaml
```

## 🎯 Casos de Uso

1. **Estandarización:** Todos los equipos usan la misma estructura de proyecto
2. **Onboarding:** Nuevos desarrolladores crean servicios sin conocer la arquitectura
3. **Governance:** Control centralizado de patrones y mejores prácticas
4. **Velocidad:** Crear nuevos servicios en minutos, no días

## 🔍 Troubleshooting

### Error: "Project not found"

Asegúrate de que el proyecto Java existe en `projects/`:

```bash
ls -la projects/
```

### Variables no reemplazadas

Verifica que el patrón de reemplazo coincida exactamente con el código:

```bash
grep -r "com.example.userservice" projects/back-ms-users-webflux/
```

### Template no aparece en Backstage

1. Verifica que `template.yaml` es válido:
   ```bash
   cat backstage-templates/webflux-service/template.yaml
   ```

2. Revisa logs de Backstage para errores de parsing

## 📚 Referencias

- [Backstage Software Templates](https://backstage.io/docs/features/software-templates/)
- [Template Actions](https://backstage.io/docs/features/software-templates/builtin-actions)
- [Writing Templates](https://backstage.io/docs/features/software-templates/writing-templates)

## 🤝 Contribuir

Para agregar soporte a nuevos tipos de proyectos:

1. Agregar lógica de detección en `generate_all()`
2. Crear nuevas plantillas en `templates/`
3. Actualizar `_reparametrize_skeleton()` con patrones específicos

---

**Autor:** Platform Engineering Team  
**Versión:** 1.0.0  
**Licencia:** MIT
