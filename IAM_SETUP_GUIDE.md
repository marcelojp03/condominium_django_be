# Guía de configuración de permisos IAM para AWS App Runner

## 🔐 PERMISOS NECESARIOS

Tu aplicación usa los siguientes servicios de AWS:
- ✅ **Amazon Rekognition** (reconocimiento facial, detección de texto, custom labels)
- ✅ **Amazon S3** (almacenamiento de imágenes)
- ✅ **Amazon Textract** (OCR de documentos)
- ✅ **Amazon RDS** (base de datos PostgreSQL)
- ✅ **Amazon ECR** (repositorio de imágenes Docker)

## 📋 PASO 1: Crear Política de IAM

### Opción A: Usando la Consola de AWS

1. Ve a IAM Console: https://console.aws.amazon.com/iam/
2. En el menú izquierdo, selecciona "Policies"
3. Click en "Create policy"
4. Selecciona la pestaña "JSON"
5. Pega la siguiente política:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "RekognitionPermissions",
            "Effect": "Allow",
            "Action": [
                "rekognition:DetectFaces",
                "rekognition:IndexFaces",
                "rekognition:SearchFaces",
                "rekognition:SearchFacesByImage",
                "rekognition:DetectText",
                "rekognition:DetectLabels",
                "rekognition:DetectCustomLabels",
                "rekognition:CompareFaces",
                "rekognition:ListCollections",
                "rekognition:ListFaces",
                "rekognition:DeleteFaces"
            ],
            "Resource": "*"
        },
        {
            "Sid": "S3Permissions",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:PutObjectAcl",
                "s3:DeleteObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::*/*",
                "arn:aws:s3:::*"
            ]
        },
        {
            "Sid": "TextractPermissions",
            "Effect": "Allow",
            "Action": [
                "textract:DetectDocumentText",
                "textract:AnalyzeDocument",
                "textract:AnalyzeExpense",
                "textract:AnalyzeID"
            ],
            "Resource": "*"
        },
        {
            "Sid": "ECRPermissions",
            "Effect": "Allow",
            "Action": [
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage"
            ],
            "Resource": "*"
        }
    ]
}
```

6. Click "Next"
7. Nombre de la política: `CondominiumBackendPolicy`
8. Descripción: "Permisos para Condominium Backend - Rekognition, S3, Textract"
9. Click "Create policy"

### Opción B: Usando AWS CLI

```powershell
# Guarda la política en un archivo JSON
$policyJson = @"
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "RekognitionPermissions",
            "Effect": "Allow",
            "Action": [
                "rekognition:DetectFaces",
                "rekognition:IndexFaces",
                "rekognition:SearchFaces",
                "rekognition:SearchFacesByImage",
                "rekognition:DetectText",
                "rekognition:DetectLabels",
                "rekognition:DetectCustomLabels",
                "rekognition:CompareFaces",
                "rekognition:ListCollections",
                "rekognition:ListFaces",
                "rekognition:DeleteFaces"
            ],
            "Resource": "*"
        },
        {
            "Sid": "S3Permissions",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:PutObjectAcl",
                "s3:DeleteObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::*/*",
                "arn:aws:s3:::*"
            ]
        },
        {
            "Sid": "TextractPermissions",
            "Effect": "Allow",
            "Action": [
                "textract:DetectDocumentText",
                "textract:AnalyzeDocument",
                "textract:AnalyzeExpense",
                "textract:AnalyzeID"
            ],
            "Resource": "*"
        },
        {
            "Sid": "ECRPermissions",
            "Effect": "Allow",
            "Action": [
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage"
            ],
            "Resource": "*"
        }
    ]
}
"@

$policyJson | Out-File -FilePath "condominium-policy.json" -Encoding UTF8

# Crear la política
aws iam create-policy `
    --policy-name CondominiumBackendPolicy `
    --policy-document file://condominium-policy.json `
    --description "Permisos para Condominium Backend"
```

## 📋 PASO 2: Crear Rol de IAM para App Runner

### Opción A: Usando la Consola de AWS

1. Ve a IAM Console: https://console.aws.amazon.com/iam/
2. En el menú izquierdo, selecciona "Roles"
3. Click en "Create role"
4. Tipo de entidad de confianza: "Custom trust policy"
5. Pega la siguiente política de confianza:

```json
{
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
}
```

6. Click "Next"
7. En "Add permissions", busca y selecciona:
   - `CondominiumBackendPolicy` (la que creaste en el Paso 1)
8. Click "Next"
9. Nombre del rol: `CondominiumAppRunnerTaskRole`
10. Descripción: "Rol de ejecución para Condominium Backend en App Runner"
11. Click "Create role"

### Opción B: Usando AWS CLI

```powershell
# Crear política de confianza
$trustPolicy = @"
{
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
}
"@

$trustPolicy | Out-File -FilePath "trust-policy.json" -Encoding UTF8

# Crear el rol
aws iam create-role `
    --role-name CondominiumAppRunnerTaskRole `
    --assume-role-policy-document file://trust-policy.json `
    --description "Rol de ejecución para Condominium Backend"

# Obtener el ARN de la política (reemplaza ACCOUNT_ID)
$accountId = aws sts get-caller-identity --query Account --output text
$policyArn = "arn:aws:iam::$accountId:policy/CondominiumBackendPolicy"

# Adjuntar la política al rol
aws iam attach-role-policy `
    --role-name CondominiumAppRunnerTaskRole `
    --policy-arn $policyArn
```

## 📋 PASO 3: Configurar App Runner con el Rol

### Si usas la Consola de AWS:

1. Ve a tu servicio en App Runner
2. En la configuración del servicio, busca "Instance role"
3. Selecciona `CondominiumAppRunnerTaskRole`
4. Guarda los cambios

### Si usas el script create-apprunner-service.ps1:

El script ya está actualizado para usar el rol. Solo necesitas:

1. Obtener el ARN del rol:
```powershell
$accountId = aws sts get-caller-identity --query Account --output text
$roleArn = "arn:aws:iam::$accountId:role/CondominiumAppRunnerTaskRole"
Write-Host "Role ARN: $roleArn"
```

2. El script lo configurará automáticamente

## 📋 PASO 4: Configurar credenciales de AWS (Opcional)

Si necesitas especificar credenciales explícitas (no recomendado, mejor usar el rol):

En las variables de entorno de App Runner:
```
AWS_ACCESS_KEY_ID=tu-access-key
AWS_SECRET_ACCESS_KEY=tu-secret-key
AWS_DEFAULT_REGION=us-east-1
```

**IMPORTANTE**: ¡NO HAGAS ESTO! Usar el rol de IAM es mucho más seguro.

## 🔍 VERIFICAR PERMISOS

Después de configurar todo, verifica:

```powershell
# Ver información del rol
aws iam get-role --role-name CondominiumAppRunnerTaskRole

# Ver políticas adjuntas al rol
aws iam list-attached-role-policies --role-name CondominiumAppRunnerTaskRole

# Ver detalles de la política
aws iam get-policy --policy-arn arn:aws:iam::ACCOUNT_ID:policy/CondominiumBackendPolicy
aws iam get-policy-version --policy-arn arn:aws:iam::ACCOUNT_ID:policy/CondominiumBackendPolicy --version-id v1
```

## ⚠️ CONSIDERACIONES DE SEGURIDAD

### 1. Principio de mínimo privilegio
Si solo usas buckets específicos de S3, limita los permisos:

```json
"Resource": [
    "arn:aws:s3:::tu-bucket-nombre/*",
    "arn:aws:s3:::tu-bucket-nombre"
]
```

### 2. Colecciones de Rekognition específicas
Si usas colecciones específicas, limita:

```json
"Resource": [
    "arn:aws:rekognition:us-east-1:ACCOUNT_ID:collection/tu-coleccion"
]
```

### 3. Proyecto Custom Labels específico
Para tu proyecto de comportamiento sospechoso:

```json
"Resource": [
    "arn:aws:rekognition:us-east-1:851725478821:project/ComportamientoSospechoso/*"
]
```

## 🔧 TROUBLESHOOTING

### Error: "Access Denied" en Rekognition
- Verifica que el rol está asignado al servicio App Runner
- Confirma que la política está adjunta al rol
- Revisa los logs de CloudWatch

### Error: "Credentials not found"
- Asegúrate de NO tener variables AWS_ACCESS_KEY_ID en el entorno
- Verifica que el rol tiene la política de confianza correcta

### Error: "Invalid bucket name"
- Verifica que los buckets de S3 existen
- Confirma que el rol tiene permisos de lectura/escritura

## 📝 CHECKLIST FINAL

- [ ] Política IAM creada: `CondominiumBackendPolicy`
- [ ] Rol IAM creado: `CondominiumAppRunnerTaskRole`
- [ ] Política adjunta al rol
- [ ] Rol asignado al servicio App Runner
- [ ] Variables AWS_ACCESS_KEY_ID NO están en el entorno
- [ ] Colecciones de Rekognition existen
- [ ] Buckets de S3 existen
- [ ] Permisos verificados
- [ ] Logs de CloudWatch configurados

## 🎯 COSTOS ADICIONALES

Con estos servicios, considera:
- **Rekognition**: ~$1 por 1,000 imágenes procesadas
- **Textract**: ~$1.50 por 1,000 páginas
- **S3**: ~$0.023 por GB/mes
- **Transferencia de datos**: Primeros 100GB gratis/mes

---

¿Preguntas? Revisa los logs de CloudWatch si algo no funciona.
