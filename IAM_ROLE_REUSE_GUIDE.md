# 🔐 Reutilización de Roles IAM - Guía Completa

## ✅ SÍ, puedes reutilizar el mismo rol IAM

Los roles IAM en AWS son **completamente reutilizables** entre diferentes servicios y aplicaciones, siempre que:

1. ✅ Tengan la **política de confianza** correcta (Trust Policy)
2. ✅ Tengan los **permisos necesarios** para todas las aplicaciones
3. ✅ El servicio AWS que lo use (App Runner) tenga permiso para asumirlo

---

## 📊 Comparación: Rol Nuevo vs Rol Existente

### Opción A: Crear Nuevo Rol ❌ (Innecesario)
```
CondominiumAppRunnerTaskRole
  ├─ Permisos: Rekognition, S3, Textract, ECR
  └─ Trust Policy: tasks.apprunner.amazonaws.com

vpay-smartdoc-apprunner-instance-role (tu rol existente)
  ├─ Permisos: Rekognition, Textract
  └─ Trust Policy: tasks.apprunner.amazonaws.com
```
**Problema:** Duplicación innecesaria, más roles que gestionar

### Opción B: Reutilizar y Extender ✅ (Recomendado)
```
vpay-smartdoc-apprunner-instance-role (actualizado)
  ├─ Permisos: Rekognition, Textract, S3, ECR
  └─ Trust Policy: tasks.apprunner.amazonaws.com
  └─ Usado por:
      ├─ vpay-smartdoc-be (App Runner)
      └─ si2-condominium-prod (App Runner)
```
**Ventaja:** Un solo rol, fácil de gestionar, menos complejidad

---

## 🔧 Tu Rol Existente

**Nombre:** `vpay-smartdoc-apprunner-instance-role`

### Permisos Actuales:
```json
{
  "rekognition:DetectText",
  "rekognition:DetectDocumentText",
  "rekognition:AnalyzeDocument",
  "textract:AnalyzeDocument",
  "textract:DetectDocumentText",
  "textract:AnalyzeExpense",
  "textract:AnalyzeID",
  "textract:GetAdapter",
  "textract:GetAdapterVersion"
}
```

### Permisos que Faltan para Condominio:
```json
{
  "rekognition:DetectFaces",        ← Reconocimiento facial
  "rekognition:IndexFaces",         ← Indexar rostros
  "rekognition:SearchFacesByImage", ← Buscar rostros
  "rekognition:DetectLabels",       ← Detectar etiquetas
  "rekognition:DetectCustomLabels", ← Comportamiento sospechoso
  "rekognition:CompareFaces",       ← Comparar rostros
  "s3:GetObject",                   ← Leer de S3
  "s3:PutObject",                   ← Guardar en S3
  "s3:DeleteObject"                 ← Eliminar de S3
}
```

---

## 🚀 Proceso de Actualización

### Paso 1: Verificar Permisos Actuales
```powershell
.\verify-iam-role.ps1
```

Esto te mostrará:
- ✅ Permisos que ya tienes
- ❌ Permisos que faltan
- 📊 Resumen por servicio

### Paso 2: Agregar Permisos Faltantes
```powershell
.\setup-iam.ps1
```

Esto agregará una **política inline** llamada `CondominiumAdditionalPermissions` con:
- Permisos de S3
- Permisos adicionales de Rekognition

### Paso 3: Verificar Actualización
```powershell
.\verify-iam-role.ps1
```

Ahora todos los permisos deberían aparecer como ✅

---

## 💡 Mejores Prácticas

### ✅ BUENAS PRÁCTICAS:

1. **Un rol por tipo de servicio/ambiente**
   ```
   vpay-smartdoc-apprunner-instance-role → Para todas las apps App Runner
   vpay-smartdoc-lambda-role → Para todas las funciones Lambda
   vpay-smartdoc-ecs-role → Para todas las tareas ECS
   ```

2. **Nombrar claramente los roles**
   ```
   {proyecto}-{servicio}-{ambiente}-role
   vpay-apprunner-production-role
   vpay-apprunner-development-role
   ```

3. **Política de mínimo privilegio**
   - Solo agregar permisos que realmente se necesitan
   - Limitar recursos cuando sea posible (buckets específicos)

4. **Documentar permisos**
   - Usar "Sid" descriptivos en las políticas
   - Comentar para qué aplicación se usa cada permiso

### ❌ MALAS PRÁCTICAS:

1. **Un rol por aplicación (innecesario)**
   ```
   condominium-role
   smartdoc-role
   app3-role
   app4-role  ← Difícil de mantener
   ```

2. **Permisos demasiado amplios**
   ```json
   {
     "Action": "*",        ← NO HACER ESTO
     "Resource": "*"
   }
   ```

3. **Hardcodear credenciales**
   ```python
   # ❌ NUNCA HACER ESTO:
   AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
   AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
   ```

---

## 📝 Estructura de tu Rol Actualizado

```json
{
  "RoleName": "vpay-smartdoc-apprunner-instance-role",
  "AssumeRolePolicyDocument": {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Service": "tasks.apprunner.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
  },
  "Policies": [
    {
      "PolicyName": "RekognitionTextractAccess",
      "PolicyDocument": {
        "Statement": [
          {
            "Sid": "RekognitionPermissions",
            "Action": [
              "rekognition:DetectText",
              "rekognition:DetectDocumentText",
              "rekognition:AnalyzeDocument"
            ]
          },
          {
            "Sid": "TextractPermissions",
            "Action": [
              "textract:*"
            ]
          }
        ]
      }
    },
    {
      "PolicyName": "CondominiumAdditionalPermissions",
      "PolicyDocument": {
        "Statement": [
          {
            "Sid": "S3Permissions",
            "Action": [
              "s3:GetObject",
              "s3:PutObject",
              "s3:DeleteObject"
            ]
          },
          {
            "Sid": "RekognitionAdditional",
            "Action": [
              "rekognition:DetectFaces",
              "rekognition:IndexFaces",
              "rekognition:SearchFacesByImage",
              "rekognition:DetectCustomLabels"
            ]
          }
        ]
      }
    }
  ]
}
```

---

## 🔍 Verificación de Permisos

### Via AWS Console:
1. IAM → Roles
2. Buscar: `vpay-smartdoc-apprunner-instance-role`
3. Tab "Permissions"
4. Ver políticas inline y managed

### Via CLI:
```powershell
# Ver información del rol
aws iam get-role --role-name vpay-smartdoc-apprunner-instance-role

# Ver políticas inline
aws iam list-role-policies --role-name vpay-smartdoc-apprunner-instance-role

# Ver detalle de una política
aws iam get-role-policy `
  --role-name vpay-smartdoc-apprunner-instance-role `
  --policy-name CondominiumAdditionalPermissions
```

---

## 🆚 Comparación de Enfoques

| Aspecto | Rol Nuevo | Rol Existente (Actualizado) |
|---------|-----------|----------------------------|
| **Gestión** | Más compleja | Más simple |
| **Costos** | Sin cambio | Sin cambio |
| **Seguridad** | Igual | Igual |
| **Mantenimiento** | 2 roles a mantener | 1 rol a mantener |
| **Permisos** | Duplicados parcialmente | Consolidados |
| **Auditoría** | Más difícil | Más fácil |
| **Recomendado** | ❌ | ✅ |

---

## 🎯 Decisión Final: Reutilizar

**Razones:**

1. ✅ **Simplicidad:** Un solo rol para todas las apps App Runner
2. ✅ **Menos gestión:** Menos roles = menos complejidad
3. ✅ **Permisos consolidados:** Fácil ver qué tiene acceso
4. ✅ **Sin duplicación:** No repetir permisos comunes
5. ✅ **Misma seguridad:** Políticas de confianza idénticas

**Tu configuración actualizada:**
```powershell
# Variables en create-apprunner-service.ps1
$IAM_ROLE_NAME = "vpay-smartdoc-apprunner-instance-role"  # ✅ Usando rol existente
```

---

## 📚 Scripts Actualizados

1. **`verify-iam-role.ps1`** - Verifica permisos actuales
2. **`setup-iam.ps1`** - Agrega permisos faltantes
3. **`create-apprunner-service.ps1`** - Usa el rol existente

---

## ✅ Checklist

- [ ] Ejecutar `.\verify-iam-role.ps1` para ver estado actual
- [ ] Ejecutar `.\setup-iam.ps1` para agregar permisos
- [ ] Verificar que todos los permisos están presentes
- [ ] Usar el rol en ambas aplicaciones:
  - vpay-smartdoc-be ✅
  - si2-condominium-prod ✅

---

## 🔒 Seguridad

**No hay riesgo** en compartir el rol entre aplicaciones porque:

1. Ambas apps están en la **misma cuenta AWS**
2. Ambas apps son **tuyas** (mismo equipo/proyecto)
3. Ambas apps necesitan **servicios similares** (Rekognition, Textract)
4. El rol **solo** puede ser asumido por App Runner (Trust Policy)

**Sí habría riesgo si:**
- Apps de diferentes clientes/proyectos
- Apps en diferentes cuentas AWS
- Apps con requisitos de seguridad muy diferentes

---

## 💰 Costos

**Roles IAM:** GRATIS ✅
- No hay cargo por roles
- No hay cargo por políticas
- No hay límite de roles (hasta 1000 por cuenta)

---

¿Alguna duda sobre reutilización de roles? Este enfoque es estándar y recomendado por AWS.
