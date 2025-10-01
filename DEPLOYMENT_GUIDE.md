# Guía paso a paso para desplegar en AWS App Runner

## Pasos previos realizados:
✅ Dockerfile creado
✅ .dockerignore creado
✅ requirements.txt actualizado con gunicorn
✅ settings.py configurado para producción

## PASO 1: Configurar AWS CLI

Instala AWS CLI si no lo tienes:
```powershell
# Descarga desde: https://aws.amazon.com/cli/
# O con chocolatey:
choco install awscli
```

Configura tus credenciales:
```powershell
aws configure
# Ingresa:
# - AWS Access Key ID
# - AWS Secret Access Key
# - Default region name (ej: us-east-1)
# - Default output format (json)
```

## PASO 2: Modificar el script deploy-to-ecr.ps1

Abre `deploy-to-ecr.ps1` y modifica estas variables:
```powershell
$AWS_ACCOUNT_ID = "TU_ACCOUNT_ID"  # Tu Account ID de AWS (12 dígitos)
$AWS_REGION = "us-east-1"          # Tu región preferida
$ECR_REPOSITORY_NAME = "condominium-backend"  # Nombre del repo
```

Para obtener tu Account ID:
```powershell
aws sts get-caller-identity --query Account --output text
```

## PASO 3: Construir y subir la imagen

Ejecuta el script:
```powershell
cd "C:\UAGRM\Sistemas de informacion 2\semestre-2-2025\primer-parcial\condominium_django_be"
.\deploy-to-ecr.ps1
```

Este script:
1. Construye la imagen Docker
2. Autentica con AWS ECR
3. Crea el repositorio ECR (si no existe)
4. Sube la imagen a ECR
5. Te muestra la URI de la imagen

## PASO 4: Crear servicio en AWS App Runner

### Opción A: Usando la consola de AWS

1. Ve a AWS App Runner: https://console.aws.amazon.com/apprunner/
2. Click en "Create service"
3. Selecciona "Container registry" → "Amazon ECR"
4. Busca y selecciona tu imagen: `condominium-backend:latest`
5. En "Deployment settings":
   - Deployment trigger: Manual o Automatic
6. Click "Next"
7. Configura el servicio:
   - Service name: `condominium-backend`
   - Virtual CPU: 1 vCPU
   - Memory: 2 GB
   - Port: 8000
8. En "Environment variables" añade:
   ```
   SECRET_KEY = tu-secret-key-segura
   DEBUG = False
   ALLOWED_HOSTS = *
   DB_NAME = vpayDB
   DB_USER = postgres
   DB_PASSWORD = postgres
   DB_HOST = dbvpay.cfiek6gqkqd5.us-east-1.rds.amazonaws.com
   DB_PORT = 5432
   CORS_ALLOW_ALL_ORIGINS = True
   ```
9. En "Health check":
   - Protocol: HTTP
   - Path: /admin/ o /api/docs/
10. Click "Create & deploy"

### Opción B: Usando AWS CLI

```powershell
# Primero, obtén la URI de tu imagen
$IMAGE_URI = "TU_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/condominium-backend:latest"

# Crea el servicio
aws apprunner create-service `
  --service-name condominium-backend `
  --source-configuration '{
    "ImageRepository": {
      "ImageIdentifier": "'$IMAGE_URI'",
      "ImageConfiguration": {
        "Port": "8000",
        "RuntimeEnvironmentVariables": {
          "SECRET_KEY": "tu-secret-key-segura",
          "DEBUG": "False",
          "ALLOWED_HOSTS": "*"
        }
      },
      "ImageRepositoryType": "ECR"
    },
    "AutoDeploymentsEnabled": false
  }' `
  --instance-configuration '{
    "Cpu": "1 vCPU",
    "Memory": "2 GB"
  }' `
  --region us-east-1
```

## PASO 5: Configurar Health Check

Tu aplicación debe responder en el endpoint de health check.
Crea un endpoint simple en Django si no tienes uno:

En `be_condominium/urls.py` añade:
```python
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "healthy"}, status=200)

urlpatterns = [
    path('health/', health_check),
    # ... resto de urls
]
```

## PASO 6: Verificar el despliegue

Una vez desplegado, App Runner te dará una URL como:
```
https://xyz123.us-east-1.awsapprunner.com
```

Prueba tu API:
- Swagger: https://xyz123.us-east-1.awsapprunner.com/api/docs/
- Admin: https://xyz123.us-east-1.awsapprunner.com/admin/

## PASO 7: Actualizar la aplicación

Cuando hagas cambios:
```powershell
# 1. Reconstruir y subir nueva imagen
.\deploy-to-ecr.ps1

# 2. Actualizar el servicio en App Runner
aws apprunner start-deployment --service-arn TU_SERVICE_ARN --region us-east-1
```

## Troubleshooting

### Error: "Task failed to start"
- Verifica las variables de entorno
- Revisa los logs en CloudWatch
- Verifica que el puerto 8000 esté expuesto

### Error de conexión a base de datos
- Verifica que el Security Group de RDS permita conexiones desde App Runner
- Configura el VPC connector si es necesario

### Imágenes de usuarios no se cargan
- Considera usar S3 para archivos media
- Configura django-storages con boto3

## Costos aproximados

AWS App Runner cobra por:
- vCPU: ~$0.064/hora para 1 vCPU
- Memoria: ~$0.007/hora por GB
- Tráfico: Primeros 100GB gratis/mes

Ejemplo: 1 vCPU + 2GB = ~$0.078/hora ≈ $56/mes (uso continuo)

## Seguridad adicional

1. Genera un SECRET_KEY seguro:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

2. Configura HTTPS (App Runner lo hace automáticamente)

3. Limita ALLOWED_HOSTS a tu dominio real

4. Configura CORS apropiadamente en producción
