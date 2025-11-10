# 📖 Instrucciones de Importación en Backstage

## Método Recomendado: app-config.yaml

Edita el archivo `app-config.yaml` en tu instancia de Backstage:

```yaml
catalog:
  locations:
    # Golden Path Templates
    - type: file
      target: ../../backstage-templates/
      rules:
        - allow: [Template]
```

**Reinicia Backstage:**
```bash
yarn dev
```

## Alternativa: URLs Individuales

Si los templates están en GitHub:

```yaml
catalog:
  locations:
    - type: url
      target: https://github.com/addon-ai/boiler-plate-code-gen/blob/main/backstage-templates/springboot-service/template.yaml
      rules:
        - allow: [Template]
    
    - type: url
      target: https://github.com/addon-ai/boiler-plate-code-gen/blob/main/backstage-templates/webflux-service/template.yaml
      rules:
        - allow: [Template]
```

## Verificación

1. Abre Backstage: `http://localhost:3000`
2. Ve a **"Create"**
3. Deberías ver:
   - **Java Springboot Service**
   - **Java Webflux Service**

## Configuración Incluida

- ✅ Organización GitHub: `addon-ai` (desde params.json)
- ✅ Group ID por defecto: `com.example`
- ✅ Java version: `21`
- ✅ Sintaxis correcta: `${{ parameters.* }}`
