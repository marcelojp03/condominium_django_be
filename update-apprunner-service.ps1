# Script para actualizar un servicio existente en App Runner
# Usa este script cuando hagas cambios y quieras redesplegar

# Variables
$AWS_REGION = "us-east-1"
$AWS_ACCOUNT_ID = "851725478821"
$SERVICE_NAME = "si2-condominium-prod"
$SERVICE_ARN = "arn:aws:apprunner:us-east-1:851725478821:service/si2-condominium-prod/7e554faed3424ab4b5f00af4b540db3c"

Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     🔄 Actualizando Condominium Backend en App Runner         ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

Write-Host "Servicio: $SERVICE_NAME" -ForegroundColor White
Write-Host "Región:   $AWS_REGION" -ForegroundColor White
Write-Host ""

Write-Host "=== Paso 1: Reconstruyendo y subiendo nueva imagen a ECR ===" -ForegroundColor Green
.\deploy-to-ecr.ps1

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n=== Paso 2: Desplegando nueva versión en App Runner ===" -ForegroundColor Green
    Write-Host "Iniciando despliegue..." -ForegroundColor Yellow
    
    aws apprunner start-deployment --service-arn $SERVICE_ARN --region $AWS_REGION
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
        Write-Host "║           ✅ Despliegue iniciado exitosamente                  ║" -ForegroundColor Green
        Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
        
        Write-Host "`n📊 Monitoreando despliegue..." -ForegroundColor Cyan
        Write-Host "Esto puede tomar 2-5 minutos...`n" -ForegroundColor Yellow
        
        # Esperar y verificar estado
        $maxAttempts = 30
        $attempt = 0
        $deployed = $false
        
        while ($attempt -lt $maxAttempts -and -not $deployed) {
            Start-Sleep -Seconds 10
            $attempt++
            
            $status = aws apprunner describe-service `
                --service-arn $SERVICE_ARN `
                --region $AWS_REGION `
                --query 'Service.Status' `
                --output text
            
            Write-Host "[$attempt/$maxAttempts] Estado: $status" -ForegroundColor Gray
            
            if ($status -eq "RUNNING") {
                $deployed = $true
                Write-Host "`n✅ Servicio desplegado y ejecutándose!" -ForegroundColor Green
            } elseif ($status -eq "OPERATION_IN_PROGRESS") {
                Write-Host "  Desplegando..." -ForegroundColor Yellow
            } elseif ($status -eq "CREATE_FAILED" -or $status -eq "UPDATE_FAILED") {
                Write-Host "`n❌ Error en el despliegue. Estado: $status" -ForegroundColor Red
                break
            }
        }
        
        # Obtener URL del servicio
        Write-Host "`n=== Información del Servicio ===" -ForegroundColor Cyan
        $serviceUrl = aws apprunner describe-service `
            --service-arn $SERVICE_ARN `
            --region $AWS_REGION `
            --query 'Service.ServiceUrl' `
            --output text
        
        Write-Host "URL: https://$serviceUrl" -ForegroundColor White
        Write-Host ""
        Write-Host "🔗 Endpoints disponibles:" -ForegroundColor Cyan
        Write-Host "  Health:  https://$serviceUrl/health/" -ForegroundColor Gray
        Write-Host "  API:     https://$serviceUrl/api/docs/" -ForegroundColor Gray
        Write-Host "  Admin:   https://$serviceUrl/admin/" -ForegroundColor Gray
        
        Write-Host "`n📊 Ver más detalles en:" -ForegroundColor Yellow
        Write-Host "https://console.aws.amazon.com/apprunner/home?region=$AWS_REGION#/services/$SERVICE_NAME" -ForegroundColor Cyan
        
    } else {
        Write-Host "`n❌ Error al iniciar el despliegue" -ForegroundColor Red
        Write-Host "Verifica el ARN del servicio y tus permisos AWS" -ForegroundColor Yellow
    }
} else {
    Write-Host "`n❌ Error al construir/subir la imagen a ECR" -ForegroundColor Red
    Write-Host "Revisa los errores anteriores" -ForegroundColor Yellow
}
