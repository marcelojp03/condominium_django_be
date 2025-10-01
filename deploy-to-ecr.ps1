# Script para construir y subir imagen Docker a AWS ECR
# Asegúrate de tener AWS CLI configurado con tus credenciales

# Variables - MODIFICA ESTOS VALORES
$AWS_REGION = "us-east-1"
$AWS_ACCOUNT_ID = "851725478821"
$ECR_REPOSITORY_NAME = "si2-condominium-be"
$IMAGE_TAG = "latest"

Write-Host "=== Paso 1: Construyendo imagen Docker ===" -ForegroundColor Green
docker build -t $ECR_REPOSITORY_NAME`:$IMAGE_TAG .

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error al construir la imagen Docker" -ForegroundColor Red
    exit 1
}

Write-Host "`n=== Paso 2: Autenticando Docker con ECR ===" -ForegroundColor Green
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error al autenticar con ECR" -ForegroundColor Red
    exit 1
}

Write-Host "`n=== Paso 3: Creando repositorio ECR (si no existe) ===" -ForegroundColor Green
aws ecr describe-repositories --repository-names $ECR_REPOSITORY_NAME --region $AWS_REGION 2>$null

if ($LASTEXITCODE -ne 0) {
    Write-Host "Repositorio no existe, creándolo..." -ForegroundColor Yellow
    aws ecr create-repository --repository-name $ECR_REPOSITORY_NAME --region $AWS_REGION
}

Write-Host "`n=== Paso 4: Etiquetando imagen para ECR ===" -ForegroundColor Green
docker tag "$ECR_REPOSITORY_NAME`:$IMAGE_TAG" "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY_NAME`:$IMAGE_TAG"

Write-Host "`n=== Paso 5: Subiendo imagen a ECR ===" -ForegroundColor Green
docker push "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY_NAME`:$IMAGE_TAG"

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n=== ✅ Imagen subida exitosamente ===" -ForegroundColor Green
    Write-Host "URI de la imagen: $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY_NAME`:$IMAGE_TAG" -ForegroundColor Cyan
    Write-Host "`nAhora puedes usar esta URI en AWS App Runner" -ForegroundColor Yellow
} else {
    Write-Host "`n=== ❌ Error al subir la imagen ===" -ForegroundColor Red
    exit 1
}
