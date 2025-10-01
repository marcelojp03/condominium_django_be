# Script para crear automáticamente el servicio en AWS App Runner
# Ejecuta este script DESPUÉS de subir la imagen a ECR

# Variables - MODIFICA ESTOS VALORES
$AWS_REGION = "us-east-1"
$AWS_ACCOUNT_ID = "851725478821"  # Reemplaza con tu Account ID
$ECR_REPOSITORY_NAME = "si2-condominium-be"
$IMAGE_TAG = "latest"
$SERVICE_NAME = "si2-condominium-prod"
$IAM_ROLE_NAME = "vpay-smartdoc-apprunner-instance-role"  # Usando tu rol existente

Write-Host "=== Configurando servicio en App Runner ===" -ForegroundColor Cyan

# Obtener Account ID si no está configurado
if ($AWS_ACCOUNT_ID -eq "TU_ACCOUNT_ID") {
    Write-Host "`Obteniendo Account ID automáticamente..." -ForegroundColor Yellow
    $AWS_ACCOUNT_ID = aws sts get-caller-identity --query Account --output text
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: No se pudo obtener el Account ID" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Account ID: $AWS_ACCOUNT_ID" -ForegroundColor Green
}

# Verificar que el rol IAM existe
Write-Host "`n=== Verificando rol IAM ===" -ForegroundColor Green
$ROLE_ARN = "arn:aws:iam::$AWS_ACCOUNT_ID`:role/$IAM_ROLE_NAME"
$roleExists = aws iam get-role --role-name $IAM_ROLE_NAME 2>$null

if ($LASTEXITCODE -ne 0) {
    Write-Host "El rol $IAM_ROLE_NAME no existe." -ForegroundColor Yellow
    Write-Host "Ejecutando setup-iam.ps1 para crear los permisos necesarios..." -ForegroundColor Yellow
    .\setup-iam.ps1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error al crear el rol IAM" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✅ Rol IAM encontrado: $ROLE_ARN" -ForegroundColor Green
}

# Genera una SECRET_KEY (o usa una existente)
Write-Host "`n=== Generando SECRET_KEY ===" -ForegroundColor Green
$SECRET_KEY = python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
Write-Host "SECRET_KEY generada: $SECRET_KEY" -ForegroundColor Cyan
Write-Host "GUARDA ESTA SECRET_KEY EN UN LUGAR SEGURO!" -ForegroundColor Yellow

$IMAGE_URI = "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY_NAME`:$IMAGE_TAG"

Write-Host "`n=== Creando servicio en App Runner ===" -ForegroundColor Green
Write-Host "Imagen: $IMAGE_URI" -ForegroundColor Cyan
Write-Host "Rol IAM: $ROLE_ARN" -ForegroundColor Cyan

# Crear el archivo de configuración JSON temporal
$configJson = @"
{
  "ServiceName": "$SERVICE_NAME",
  "SourceConfiguration": {
    "ImageRepository": {
      "ImageIdentifier": "$IMAGE_URI",
      "ImageConfiguration": {
        "Port": "8000",
        "RuntimeEnvironmentVariables": {
          "SECRET_KEY": "$SECRET_KEY",
          "DEBUG": "False",
          "ALLOWED_HOSTS": "*",
          "DB_NAME": "vpayDB",
          "DB_USER": "postgres",
          "DB_PASSWORD": "postgres",
          "DB_HOST": "dbvpay.cfiek6gqkqd5.us-east-1.rds.amazonaws.com",
          "DB_PORT": "5432",
          "CORS_ALLOW_ALL_ORIGINS": "True",
          "AWS_DEFAULT_REGION": "$AWS_REGION"
        }
      },
      "ImageRepositoryType": "ECR"
    },
    "AutoDeploymentsEnabled": false
  },
  "InstanceConfiguration": {
    "Cpu": "1 vCPU",
    "Memory": "2 GB",
    "InstanceRoleArn": "$ROLE_ARN"
  },
  "HealthCheckConfiguration": {
    "Protocol": "HTTP",
    "Path": "/health/",
    "Interval": 10,
    "Timeout": 5,
    "HealthyThreshold": 1,
    "UnhealthyThreshold": 5
  }
}
"@

# Guardar configuración en archivo temporal
$configJson | Out-File -FilePath "apprunner-config.json" -Encoding UTF8

Write-Host "`nCreando servicio con la siguiente configuración:" -ForegroundColor Yellow
Write-Host $configJson

# Crear el servicio
aws apprunner create-service --cli-input-json file://apprunner-config.json --region $AWS_REGION

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n=== ✅ Servicio creado exitosamente ===" -ForegroundColor Green
    Write-Host "`nEsperando a que el servicio esté disponible..." -ForegroundColor Yellow
    Write-Host "Esto puede tomar varios minutos..." -ForegroundColor Yellow
    
    # Esperar y obtener la URL del servicio
    Start-Sleep -Seconds 10
    $serviceInfo = aws apprunner list-services --region $AWS_REGION | ConvertFrom-Json
    $serviceArn = $serviceInfo.ServiceSummaryList | Where-Object { $_.ServiceName -eq $SERVICE_NAME } | Select-Object -ExpandProperty ServiceArn
    
    if ($serviceArn) {
        Write-Host "`nService ARN: $serviceArn" -ForegroundColor Cyan
        Write-Host "`nPara ver el estado:" -ForegroundColor Yellow
        Write-Host "aws apprunner describe-service --service-arn $serviceArn --region $AWS_REGION" -ForegroundColor Cyan
        
        Write-Host "`nPara obtener la URL del servicio:" -ForegroundColor Yellow
        Write-Host "aws apprunner describe-service --service-arn $serviceArn --region $AWS_REGION --query 'Service.ServiceUrl' --output text" -ForegroundColor Cyan
    }
    
    Write-Host "`n=== Información importante ===" -ForegroundColor Green
    Write-Host "SECRET_KEY: $SECRET_KEY" -ForegroundColor Cyan
    Write-Host "GUARDA ESTA CLAVE - La necesitarás para futuras actualizaciones" -ForegroundColor Yellow
    
    Write-Host "`n=== Permisos configurados ===" -ForegroundColor Cyan
    Write-Host "  Amazon Rekognition (reconocimiento facial, detección de texto)" -ForegroundColor Green
    Write-Host "  Amazon S3 (almacenamiento de imágenes)" -ForegroundColor Green
    Write-Host "  Amazon Textract (OCR de documentos)" -ForegroundColor Green
    Write-Host "  Amazon ECR (pull de imágenes)" -ForegroundColor Green
    
} else {
    Write-Host "`n=== Error al crear el servicio ===" -ForegroundColor Red
}

# Limpiar archivo temporal
Remove-Item "apprunner-config.json" -ErrorAction SilentlyContinue

Write-Host "`nPara monitorear el despliegue, ve a:" -ForegroundColor Yellow
Write-Host "https://console.aws.amazon.com/apprunner/home?region=$AWS_REGION#/services" -ForegroundColor Cyan
