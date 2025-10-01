# Comandos rápidos para desarrollo y despliegue

function Show-Menu {
    Write-Host "`n=== CONDOMINIUM BACKEND - MENU ===" -ForegroundColor Cyan
    Write-Host "1. Configurar IAM (Rekognition, S3, Textract)"
    Write-Host "2. Probar Docker localmente"
    Write-Host "3. Desplegar a AWS ECR (primera vez)"
    Write-Host "4. 🔄 Actualizar App Runner (después de cambios)"
    Write-Host "5. Ejecutar servidor local (Django)"
    Write-Host "6. Ver logs de Docker local"
    Write-Host "7. Generar SECRET_KEY nueva"
    Write-Host "8. Obtener Account ID de AWS"
    Write-Host "9. Ver estado del servicio App Runner"
    Write-Host "10. Verificar rol IAM"
    Write-Host "0. Salir"
    Write-Host "================================`n" -ForegroundColor Cyan
}

function Setup-IAM {
    Write-Host "`nConfigurando permisos IAM..." -ForegroundColor Green
    .\setup-iam.ps1
}

function Test-DockerLocal {
    Write-Host "`nProbando Docker localmente..." -ForegroundColor Green
    docker build -t condominium-backend:test .
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✅ Imagen construida. Iniciando contenedor..." -ForegroundColor Green
        docker run -p 8000:8000 -e DEBUG=True -e ALLOWED_HOSTS=* condominium-backend:test
    }
}

function Deploy-ToECR {
    Write-Host "`nDesplegando a AWS ECR..." -ForegroundColor Green
    .\deploy-to-ecr.ps1
}

function Update-AppRunner {
    Write-Host "`nActualizando servicio en App Runner..." -ForegroundColor Green
    .\update-apprunner-service.ps1
}

function Start-LocalServer {
    Write-Host "`nIniciando servidor Django local..." -ForegroundColor Green
    Set-Location "be_condominium"
    python manage.py runserver
}

function Show-DockerLogs {
    Write-Host "`nMostrando logs de Docker..." -ForegroundColor Green
    $containerId = docker ps -q --filter ancestor=condominium-backend:test
    if ($containerId) {
        docker logs -f $containerId
    } else {
        Write-Host "No hay contenedores ejecutándose" -ForegroundColor Yellow
    }
}

function Generate-SecretKey {
    Write-Host "`nGenerando nueva SECRET_KEY..." -ForegroundColor Green
    python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
}

function Get-AWSAccountId {
    Write-Host "`nObteniendo AWS Account ID..." -ForegroundColor Green
    aws sts get-caller-identity --query Account --output text
}

function Get-AppRunnerStatus {
    Write-Host "`nIngresa el ARN de tu servicio App Runner:" -ForegroundColor Yellow
    $serviceArn = Read-Host
    aws apprunner describe-service --service-arn $serviceArn --region us-east-1
}

function Verify-IAMRole {
    Write-Host "`nVerificando rol IAM..." -ForegroundColor Green
    $accountId = aws sts get-caller-identity --query Account --output text
    $roleName = "CondominiumAppRunnerTaskRole"
    
    Write-Host "`nRol: $roleName" -ForegroundColor Cyan
    aws iam get-role --role-name $roleName
    
    Write-Host "`nPolíticas adjuntas:" -ForegroundColor Cyan
    aws iam list-attached-role-policies --role-name $roleName
}

# Main loop
do {
    Show-Menu
    $choice = Read-Host "Selecciona una opción"
    
    switch ($choice) {
        "1" { Setup-IAM }
        "2" { Test-DockerLocal }
        "3" { Deploy-ToECR }
        "4" { Update-AppRunner }
        "5" { Start-LocalServer }
        "6" { Show-DockerLogs }
        "7" { Generate-SecretKey }
        "8" { Get-AWSAccountId }
        "9" { Get-AppRunnerStatus }
        "10" { Verify-IAMRole }
        "0" { Write-Host "Saliendo..." -ForegroundColor Cyan; break }
        default { Write-Host "Opción inválida" -ForegroundColor Red }
    }
    
    if ($choice -ne "0") {
        Write-Host "`nPresiona Enter para continuar..." -ForegroundColor Yellow
        Read-Host
    }
} while ($choice -ne "0")
