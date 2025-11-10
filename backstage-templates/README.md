# 🎯 Backstage Golden Path Templates

Este directorio contiene Software Templates (Golden Paths) listos para importar en Backstage.

## 📦 Templates Disponibles

- **springboot-service** - Java Spring Boot microservice con arquitectura hexagonal
- **webflux-service** - Java Spring WebFlux microservice reactivo con arquitectura hexagonal

## 🚀 Importar en Backstage

### Opción 1: Usando el UI de Backstage (Recomendado)

1. Abre tu instancia de Backstage
2. Ve a **"Create"** → **"Register Existing Component"**
3. Ingresa la URL del `catalog-info.yaml`:
   ```
   file:///path/to/backstage-templates/catalog-info.yaml
   ```
   O si está en GitHub:
   ```
   https://github.com/tu-org/tu-repo/blob/main/backstage-templates/catalog-info.yaml
   ```
4. Click en **"Analyze"**
5. Click en **"Import"**

### Opción 2: Configuración en app-config.yaml

Agrega al archivo `app-config.yaml` de Backstage:

```yaml
catalog:
  locations:
    # Golden Path Templates
    - type: file
      target: /path/to/backstage-templates/catalog-info.yaml
```

Luego reinicia Backstage:
```bash
yarn dev
```

### Opción 3: Usando Backstage CLI

```bash
# Desde el directorio de Backstage
yarn backstage-cli catalog:import \
  --location file:///path/to/backstage-templates/catalog-info.yaml
```

## 🎨 Usar los Templates

Una vez importados:

1. Ve a **"Create"** en Backstage
2. Verás los templates:
   - **Java Springboot Service**
   - **Java Webflux Service**
3. Selecciona uno y completa el formulario:
   - **Component ID**: `payment-service`
   - **Group ID**: `com.bank.payments`
   - **Owner**: `payments-team`
   - **Description**: `Payment processing service`
4. Click en **"Create"**

Backstage automáticamente:
- ✅ Genera el proyecto con tus valores
- ✅ Crea el repositorio en GitHub
- ✅ Hace commit inicial
- ✅ Registra el componente en el catálogo
- ✅ Configura CI/CD workflows

## 📁 Estructura

```
backstage-templates/
├── catalog-info.yaml          # ← Importa este archivo en Backstage
├── springboot-service/
│   ├── template.yaml          # Definición del template
│   └── skeleton/              # Proyecto plantilla
│       ├── pom.xml
│       ├── src/
│       └── ...
└── webflux-service/
    ├── template.yaml
    └── skeleton/
        ├── pom.xml
        ├── src/
        └── ...
```

## 🔧 Personalización

### Modificar Templates

1. Edita `template.yaml` para cambiar parámetros
2. Modifica `skeleton/` para cambiar el código base
3. Reimporta en Backstage (se actualizará automáticamente)

### Agregar Nuevos Parámetros

En `template.yaml`:

```yaml
parameters:
  - title: Configuración Adicional
    properties:
      database_type:
        title: Tipo de Base de Datos
        type: string
        enum:
          - postgresql
          - mysql
```

## 🧪 Validación

### Verificar Templates

```bash
# Verificar estructura
ls -la backstage-templates/

# Ver catalog-info.yaml
cat backstage-templates/catalog-info.yaml

# Verificar template.yaml
cat backstage-templates/springboot-service/template.yaml
```

### Probar Localmente

Si tienes Backstage corriendo localmente:

```bash
cd backstage/
yarn dev

# Navega a http://localhost:3000/create
# Deberías ver los templates importados
```

## 📊 Parámetros Disponibles

Los templates soportan las siguientes variables:

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `component_id` | Nombre del componente | `user-service` |
| `groupId` | Group ID de Maven | `com.example` |
| `description` | Descripción del servicio | `User management API` |
| `owner` | Equipo propietario | `platform-team` |
| `javaVersion` | Versión de Java | `21` |
| `repoUrl` | URL del repositorio | `github.com?owner=org&repo=service` |

## 🔍 Troubleshooting

### Template no aparece en Backstage

1. Verifica que el `catalog-info.yaml` fue importado:
   ```bash
   # En Backstage UI: Catalog → Locations
   ```

2. Revisa logs de Backstage:
   ```bash
   # En el directorio de Backstage
   yarn dev
   # Buscar errores en la consola
   ```

3. Valida el YAML:
   ```bash
   # Usar un validador online
   cat catalog-info.yaml | pbcopy
   # Pegar en https://www.yamllint.com/
   ```

### Error al crear proyecto

1. Verifica permisos de GitHub token
2. Asegúrate que el skeleton tiene todos los archivos
3. Revisa que las variables en `template.yaml` coinciden con el skeleton

## 📚 Recursos

- [Backstage Software Templates](https://backstage.io/docs/features/software-templates/)
- [Writing Templates](https://backstage.io/docs/features/software-templates/writing-templates)
- [Template Actions](https://backstage.io/docs/features/software-templates/builtin-actions)

## 🤝 Soporte

Para problemas o preguntas:
1. Revisar logs de Backstage
2. Verificar que el `catalog-info.yaml` es válido
3. Contactar al equipo de Platform Engineering

---

**Generado automáticamente por:** `py-backstage-goldenpath-gen`  
**Fecha:** Noviembre 2025
