# 🎯 Integración con Backstage - Golden Paths

## Resumen Ejecutivo

Se ha creado una nueva librería **`py-backstage-goldenpath-gen`** que transforma proyectos Java generados en **Software Templates de Backstage** (Golden Paths), completando el ciclo de Platform Engineering.

## 🔄 Flujo Completo del Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    CODE GENERATION PIPELINE                      │
└─────────────────────────────────────────────────────────────────┘

1. Smithy Definitions
   ↓
2. pyjava-springboot-backend-codegen / pyjava-webflux-backend-codegen
   ↓
3. Proyectos Java (projects/)
   ├── back-ms-users-webflux/
   ├── back-ms-users-springboot/
   └── ...
   ↓
4. py-backstage-goldenpath-gen  ← NUEVO
   ↓
5. Backstage Templates (backstage-templates/)
   ├── webflux-service/
   │   ├── template.yaml
   │   └── skeleton/
   └── springboot-service/
       ├── template.yaml
       └── skeleton/
   ↓
6. Backstage UI (Desarrolladores crean servicios)
```

## 📦 Nueva Librería: `py-backstage-goldenpath-gen`

### Ubicación
```
libs/py-backstage-goldenpath-gen/
├── templates/
│   ├── template.yaml.mustache
│   └── catalog-info.yaml.mustache
├── __init__.py
├── main.py
└── README.md
```

### Función Principal

**Entrada:** Proyecto Java ya generado  
**Salida:** Template de Backstage listo para registrar

### Proceso de Transformación

1. **Copia el proyecto** a `skeleton/`
2. **Re-parametriza** valores hardcodeados:
   - `back-ms-users-webflux` → `${{ values.component_id }}`
   - `com.example.userservice` → `${{ values.groupId }}`
   - Paquetes Java → `${{ values.java_package_path }}`
3. **Genera manifiestos** de Backstage:
   - `template.yaml` (definición del scaffolder)
   - `catalog-info.yaml` (metadata del componente)

## 🚀 Uso

### Ejecución Automática (Recomendado)

El pipeline ejecuta automáticamente la generación de Golden Paths:

```bash
./scripts/code-gen-pipeline.sh
```

**Salida:**
```
🎯 Step 8: Generating Backstage Golden Paths...
📦 Generating Golden Path for back-ms-users-webflux (webflux)...
✅ Golden Path created at backstage-templates/webflux-service
📦 Generating Golden Path for back-ms-users-springboot (springboot)...
✅ Golden Path created at backstage-templates/springboot-service
✅ All Golden Paths generated successfully!
```

### Ejecución Manual

```bash
python3 libs/py-backstage-goldenpath-gen/main.py \
    libs/config/params.json \
    projects/ \
    backstage-templates/
```

## 📋 Estructura de Salida

```
backstage-templates/
├── webflux-service/
│   ├── template.yaml              # Manifiesto de Backstage
│   └── skeleton/                   # Proyecto "plantilla"
│       ├── catalog-info.yaml       # Metadata del componente
│       ├── pom.xml                 # Con ${{ values.component_id }}
│       ├── src/
│       │   └── main/java/
│       │       └── ${{ values.java_package_path }}/
│       │           ├── domain/
│       │           ├── application/
│       │           └── infrastructure/
│       └── ...
└── springboot-service/
    └── ...
```

## 🎨 Template de Backstage Generado

### Parámetros Disponibles

Los desarrolladores completarán estos campos en Backstage UI:

| Parámetro | Tipo | Descripción | Ejemplo |
|-----------|------|-------------|---------|
| `component_id` | string | Nombre del componente | `user-service` |
| `description` | string | Descripción del servicio | `User management API` |
| `owner` | string | Equipo propietario | `platform-team` |
| `groupId` | string | Group ID de Maven | `com.example` |
| `javaVersion` | enum | Versión de Java | `21` |
| `repoUrl` | string | URL del repositorio | `github.com?owner=org&repo=user-service` |

### Steps del Scaffolder

1. **fetch:template** - Copia el skeleton y reemplaza variables
2. **publish:github** - Crea repositorio en GitHub
3. **catalog:register** - Registra el componente en el catálogo

## 🔗 Integración con Backstage

### 1. Registrar Templates

**Opción A: Configuración (Recomendado)**

Edita `app-config.yaml` de Backstage:

```yaml
catalog:
  locations:
    # Registrar templates automáticamente
    - type: file
      target: /path/to/backstage-templates/webflux-service/template.yaml
    - type: file
      target: /path/to/backstage-templates/springboot-service/template.yaml
```

**Opción B: UI de Backstage**

1. Ir a "Create" → "Register Existing Component"
2. Ingresar URL del `template.yaml`
3. Click en "Analyze" y "Import"

### 2. Usar los Templates

1. Ir a "Create" en Backstage
2. Seleccionar "Java WebFlux Service" o "Java SpringBoot Service"
3. Completar el formulario:
   - Nombre del componente: `payment-service`
   - Group ID: `com.bank.payments`
   - Owner: `payments-team`
   - Descripción: `Payment processing service`
4. Click en "Create"

**Backstage automáticamente:**
- ✅ Genera el proyecto con los valores ingresados
- ✅ Crea el repositorio en GitHub
- ✅ Hace commit inicial
- ✅ Registra el componente en el catálogo
- ✅ Configura CI/CD workflows

## 🎯 Beneficios

### Para Desarrolladores
- ⚡ Crear servicios en **minutos** vs días
- 📚 No necesitan conocer arquitectura hexagonal
- 🎨 Interfaz gráfica intuitiva
- ✅ Proyectos pre-configurados con mejores prácticas

### Para Platform Engineering
- 🏛️ **Governance centralizado** de patrones
- 📊 Visibilidad de todos los servicios
- 🔄 Actualizaciones de templates propagadas automáticamente
- 📈 Métricas de adopción de estándares

### Para la Organización
- 🚀 Velocidad de desarrollo aumentada
- 🎯 Estandarización de arquitectura
- 📉 Reducción de deuda técnica
- 🤝 Onboarding más rápido

## 🔧 Personalización

### Agregar Nuevos Parámetros

Edita `templates/template.yaml.mustache`:

```yaml
parameters:
  - title: Configuración de Base de Datos
    properties:
      database_type:
        title: Tipo de Base de Datos
        type: string
        enum:
          - postgresql
          - mysql
          - mongodb
```

### Modificar Reemplazos

Edita `main.py`, método `_reparametrize_skeleton()`:

```python
replacements = {
    # Agregar nuevos patrones
    'spring.datasource.url=jdbc:postgresql': 
        'spring.datasource.url=jdbc:${{ values.database_type }}',
}
```

## 📊 Ejemplo de Uso Real

### Antes (Manual)

```bash
# Desarrollador debe:
1. Clonar repositorio template
2. Buscar/reemplazar nombres manualmente
3. Actualizar pom.xml
4. Renombrar paquetes Java
5. Configurar GitHub
6. Configurar CI/CD
7. Registrar en catálogo

Tiempo: 2-4 horas
Errores: Frecuentes
```

### Después (Con Backstage)

```bash
# Desarrollador:
1. Click en "Create" en Backstage
2. Completar formulario (2 minutos)
3. Click en "Create"

Tiempo: 2 minutos
Errores: Ninguno
```

## 🧪 Validación

### Verificar Generación

```bash
# Listar templates generados
ls -la backstage-templates/

# Verificar template.yaml
cat backstage-templates/webflux-service/template.yaml

# Verificar parametrización
grep -r "values.component_id" backstage-templates/webflux-service/skeleton/
```

### Probar en Backstage Local

```bash
# Iniciar Backstage en modo desarrollo
cd backstage/
yarn dev

# Navegar a http://localhost:3000/create
# Seleccionar el template y probar
```

## 📈 Métricas de Éxito

Después de implementar Golden Paths, medir:

- ⏱️ **Tiempo de creación de servicio:** De 4 horas → 2 minutos
- 📊 **Adopción de estándares:** De 60% → 100%
- 🐛 **Errores de configuración:** De 30% → 0%
- 🚀 **Servicios creados por mes:** De 5 → 50+
- 😊 **Satisfacción de desarrolladores:** De 6/10 → 9/10

## 🔍 Troubleshooting

### Template no aparece en Backstage

1. Verificar que `template.yaml` es válido:
   ```bash
   cat backstage-templates/webflux-service/template.yaml
   ```

2. Revisar logs de Backstage:
   ```bash
   # En el directorio de Backstage
   yarn dev
   # Buscar errores en la consola
   ```

3. Verificar que la ruta en `app-config.yaml` es correcta

### Variables no se reemplazan

Verificar que el patrón existe en el código original:

```bash
grep -r "back-ms-users-webflux" projects/back-ms-users-webflux/
```

### Error al crear proyecto desde Backstage

1. Verificar permisos de GitHub token
2. Revisar que el skeleton tiene todos los archivos necesarios
3. Verificar que las variables en `template.yaml` coinciden con el skeleton

## 📚 Recursos

- [Backstage Software Templates](https://backstage.io/docs/features/software-templates/)
- [Writing Custom Templates](https://backstage.io/docs/features/software-templates/writing-templates)
- [Template Actions Reference](https://backstage.io/docs/features/software-templates/builtin-actions)
- [Backstage Best Practices](https://backstage.io/docs/overview/architecture-overview)

## 🎓 Próximos Pasos

1. **Registrar templates** en tu instancia de Backstage
2. **Capacitar equipos** en el uso de Golden Paths
3. **Recopilar feedback** de desarrolladores
4. **Iterar y mejorar** templates basado en uso real
5. **Agregar más templates** (microservicios, APIs, frontends, etc.)

## 🤝 Soporte

Para preguntas o problemas:
1. Revisar documentación en `libs/py-backstage-goldenpath-gen/README.md`
2. Verificar logs del pipeline
3. Contactar al equipo de Platform Engineering

---

**Versión:** 1.0.0  
**Fecha:** Noviembre 2025  
**Autor:** Platform Engineering Team
