# Script para crear el Access Role de App Runner (para acceso a ECR)
# Este rol permite que App Runner descargue imágenes desde ECR

$ErrorActionPreference = "Stop"

Write-Host "=== CONFIGURACIÓN DE APP RUNNER ACCESS ROLE ===" -ForegroundColor Cyan
Write-Host ""

$ROLE_NAME = "AppRunnerECRAccessRole"

# Verificar si el rol ya existe
Write-Host "Verificando si el rol existe..." -ForegroundColor Yellow
$roleExists = $false
try {
    aws iam get-role --role-name $ROLE_NAME 2>$null | Out-Null
    $roleExists = $true
    Write-Host "✓ El rol '$ROLE_NAME' ya existe" -ForegroundColor Green
} catch {
    Write-Host "✓ El rol no existe, se creará uno nuevo" -ForegroundColor Green
}

if (-not $roleExists) {
    # Crear el Trust Policy para App Runner
    Write-Host "`nCreando Trust Policy..." -ForegroundColor Yellow
    
    $trustPolicy = @"
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "build.apprunner.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
"@
    
    $trustPolicy | Out-File -FilePath "trust-policy-apprunner.json" -Encoding utf8
    
    # Crear el rol
    Write-Host "Creando rol IAM..." -ForegroundColor Yellow
    aws iam create-role `
        --role-name $ROLE_NAME `
        --assume-role-policy-document file://trust-policy-apprunner.json `
        --description "Permite a App Runner acceder a ECR para descargar imágenes Docker"
    
    Write-Host "✓ Rol creado exitosamente" -ForegroundColor Green
    
    # Adjuntar la política administrada de AWS para ECR
    Write-Host "`nAdjuntando política de acceso a ECR..." -ForegroundColor Yellow
    aws iam attach-role-policy `
        --role-name $ROLE_NAME `
        --policy-arn "arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess"
    
    Write-Host "✓ Política adjuntada exitosamente" -ForegroundColor Green
    
    # Limpiar archivo temporal
    Remove-Item "trust-policy-apprunner.json" -ErrorAction SilentlyContinue
}

# Obtener el ARN del rol
Write-Host "`nObteniendo ARN del rol..." -ForegroundColor Yellow
$roleArn = aws iam get-role --role-name $ROLE_NAME --query "Role.Arn" --output text

Write-Host ""
Write-Host "=== CONFIGURACIÓN COMPLETADA ===" -ForegroundColor Green
Write-Host ""
Write-Host "📋 RESUMEN DE ROLES PARA APP RUNNER:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1️⃣  ACCESS ROLE (para acceso a ECR):" -ForegroundColor Yellow
Write-Host "   Nombre: $ROLE_NAME" -ForegroundColor White
Write-Host "   ARN: $roleArn" -ForegroundColor White
Write-Host ""
Write-Host "2️⃣  INSTANCE ROLE (para servicios AWS):" -ForegroundColor Yellow
Write-Host "   Nombre: vpay-smartdoc-apprunner-instance-role" -ForegroundColor White
Write-Host ""
Write-Host "=== PRÓXIMOS PASOS ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Al crear el servicio en App Runner:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. En 'Source':" -ForegroundColor White
Write-Host "   - Repository type: Container registry" -ForegroundColor Gray
Write-Host "   - Provider: Amazon ECR" -ForegroundColor Gray
Write-Host "   - ECR access role: Selecciona '$ROLE_NAME' ✓" -ForegroundColor Green
Write-Host ""
Write-Host "2. En 'Security > Instance role':" -ForegroundColor White
Write-Host "   - Selecciona 'vpay-smartdoc-apprunner-instance-role' ✓" -ForegroundColor Green
Write-Host ""
Write-Host "💡 Ahora deberías ver ambos roles en la consola de App Runner" -ForegroundColor Cyan
Write-Host ""
