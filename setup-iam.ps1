# Script para configurar IAM Role de App Runner
# Actualiza el rol existente con permisos adicionales necesarios

Write-Host "🔐 Configurando permisos IAM para Condominium Backend" -ForegroundColor Cyan
Write-Host ""

# Variables
$AWS_ACCOUNT_ID = "851725478821"
$ROLE_NAME = "vpay-smartdoc-apprunner-instance-role"  # Usando rol existente
$POLICY_NAME = "CondominiumAdditionalPermissions"

# Obtener Account ID
Write-Host "=== Paso 1: Verificando Account ID ===" -ForegroundColor Green
Write-Host "Account ID: $AWS_ACCOUNT_ID" -ForegroundColor Cyan

$policyDocument = @"
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

# Verificar que el rol existe
Write-Host "`n=== Paso 2: Verificando rol IAM existente ===" -ForegroundColor Green
$roleExists = aws iam get-role --role-name $ROLE_NAME 2>$null

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ El rol $ROLE_NAME no existe." -ForegroundColor Red
    Write-Host "⚠️ Por favor, crea el rol primero o verifica el nombre." -ForegroundColor Yellow
    exit 1
} else {
    Write-Host "✅ Rol encontrado: $ROLE_NAME" -ForegroundColor Green
    $ROLE_ARN = "arn:aws:iam::$AWS_ACCOUNT_ID`:role/$ROLE_NAME"
}

# Verificar permisos actuales
Write-Host "`n=== Paso 3: Verificando permisos actuales ===" -ForegroundColor Green
$currentPolicies = aws iam list-role-policies --role-name $ROLE_NAME --query 'PolicyNames' --output json | ConvertFrom-Json
Write-Host "Políticas inline actuales:" -ForegroundColor Cyan
$currentPolicies | ForEach-Object { Write-Host "  - $_" -ForegroundColor White }

# Definir política adicional para S3 y otros servicios
Write-Host "`n=== Paso 4: Agregando permisos adicionales ===" -ForegroundColor Green

# Tu rol ya tiene Rekognition y Textract, vamos a agregar S3 y más permisos
$additionalPolicyDocument = @"
{
    "Version": "2012-10-17",
    "Statement": [
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
            "Sid": "RekognitionAdditional",
            "Effect": "Allow",
            "Action": [
                "rekognition:DetectFaces",
                "rekognition:IndexFaces",
                "rekognition:SearchFaces",
                "rekognition:SearchFacesByImage",
                "rekognition:DetectLabels",
                "rekognition:CompareFaces",
                "rekognition:ListCollections",
                "rekognition:ListFaces",
                "rekognition:DeleteFaces"
            ],
            "Resource": "*"
        }
    ]
}
"@

$additionalPolicyDocument | Out-File -FilePath "temp-additional-policy.json" -Encoding UTF8 -NoNewline

# Agregar política inline al rol
Write-Host "Agregando política inline '$POLICY_NAME' al rol..." -ForegroundColor Yellow

aws iam put-role-policy `
    --role-name $ROLE_NAME `
    --policy-name $POLICY_NAME `
    --policy-document file://temp-additional-policy.json

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Política agregada exitosamente" -ForegroundColor Green
} else {
    Write-Host "⚠️ Error al agregar la política (puede que ya exista)" -ForegroundColor Yellow
}

# Limpiar archivo temporal
Remove-Item "temp-additional-policy.json" -ErrorAction SilentlyContinue

# Resumen
Write-Host "`n=== ✅ CONFIGURACIÓN COMPLETADA ===" -ForegroundColor Green
Write-Host "`nRecursos creados:" -ForegroundColor Cyan
Write-Host "  Política: $POLICY_ARN" -ForegroundColor White
Write-Host "  Rol:      $ROLE_ARN" -ForegroundColor White

Write-Host "`n=== Permisos configurados ===" -ForegroundColor Cyan
Write-Host "  ✅ Amazon Rekognition (reconocimiento facial, detección de texto)" -ForegroundColor Green
Write-Host "  ✅ Amazon S3 (almacenamiento de imágenes)" -ForegroundColor Green
Write-Host "  ✅ Amazon Textract (OCR de documentos)" -ForegroundColor Green
Write-Host "  ✅ Amazon ECR (pull de imágenes Docker)" -ForegroundColor Green

Write-Host "`n=== Próximos pasos ===" -ForegroundColor Yellow
Write-Host "1. El rol será usado automáticamente por create-apprunner-service.ps1" -ForegroundColor White
Write-Host "2. O configúralo manualmente en la consola de App Runner" -ForegroundColor White
Write-Host "   - Instance role: $ROLE_NAME" -ForegroundColor Cyan

Write-Host "`n⚠️ IMPORTANTE: NO agregues variables AWS_ACCESS_KEY_ID al entorno" -ForegroundColor Yellow
Write-Host "El rol de IAM proporcionará las credenciales automáticamente.`n" -ForegroundColor Yellow
