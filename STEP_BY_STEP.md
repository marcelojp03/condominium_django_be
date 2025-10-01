# 🚀 DESPLIEGUE EN AWS - PROCESO COMPLETO

## 📋 CHECKLIST PREVIO

- [ ] Docker Desktop instalado y ejecutándose
- [ ] AWS CLI instalado (`aws --version`)
- [ ] Credenciales AWS configuradas (`aws configure`)
- [ ] Obtener tu AWS Account ID: `aws sts get-caller-identity --query Account --output text`
- [ ] Python instalado (para generar SECRET_KEY)

---

## 🎯 PROCESO PASO A PASO

### PASO 1: Preparar el proyecto ✅ (YA HECHO)

Los siguientes archivos ya están creados:
- ✅ `Dockerfile` - Configuración de Docker
- ✅ `.dockerignore` - Archivos a excluir
- ✅ `requirements.txt` - Dependencias (con gunicorn)
- ✅ `settings.py` - Configurado para producción
- ✅ `urls.py` - Con endpoint /health/

---

### PASO 2: Configurar permisos IAM (NUEVO - IMPORTANTE) 🔐

Tu aplicación usa **Rekognition**, **Textract** y **S3**, por lo que necesita permisos especiales.

**Ejecuta el script automatizado:**
```powershell
.\setup-iam.ps1
```

Este script crea automáticamente:
- ✅ Política IAM con permisos para Rekognition, S3, Textract
- ✅ Rol IAM para App Runner
- ✅ Vincula la política al rol

**O sigue la guía manual:** Lee `IAM_SETUP_GUIDE.md`

⚠️ **IMPORTANTE**: NO necesitas configurar AWS_ACCESS_KEY_ID en las variables de entorno. El rol de IAM proveerá las credenciales automáticamente.

---

### PASO 3: Configurar scripts de despliegue

**Edita `deploy-to-ecr.ps1`:**
```powershell
$AWS_ACCOUNT_ID = "123456789012"  # ← Cambia esto
$AWS_REGION = "us-east-1"          # ← Tu región
```

**Edita `create-apprunner-service.ps1`:**
```powershell
$AWS_ACCOUNT_ID = "123456789012"  # ← El mismo de arriba
```

---

### PASO 4: Probar localmente (OPCIONAL)

```powershell
# Opción A: Script automatizado
.\test-docker-local.ps1

# Opción B: Manual
docker build -t condominium-backend:test .
docker run -p 8000:8000 -e DEBUG=True condominium-backend:test

# Probar en: http://localhost:8000/api/docs/
```

---

### PASO 5: Subir imagen a ECR

```powershell
.\deploy-to-ecr.ps1
```

Este script:
1. ✅ Construye la imagen Docker
2. ✅ Autentica con AWS ECR
3. ✅ Crea repositorio (si no existe)
4. ✅ Sube la imagen
5. ✅ Te da la URI de la imagen

**Output esperado:**
```
URI de la imagen: 123456789012.dkr.ecr.us-east-1.amazonaws.com/condominium-backend:latest
```

---

### PASO 6: Crear servicio en App Runner

#### OPCIÓN A: Script automático (Recomendado)

```powershell
.\create-apprunner-service.ps1
```

Este script:
- ✅ Verifica que el rol IAM existe (o lo crea automáticamente)
- ✅ Crea el servicio con puerto 8000
- ✅ Configura health check en /health/
- ✅ Asigna el rol IAM con permisos para Rekognition, S3, Textract
- ✅ Genera SECRET_KEY automáticamente
- ✅ Configura todas las variables de entorno

#### OPCIÓN B: Consola de AWS

1. Ve a: https://console.aws.amazon.com/apprunner/
2. Click "Create service"
3. Selecciona "Container registry" → "Amazon ECR"
4. Elige tu imagen: `condominium-backend:latest`
5. Configura:
   - **Port:** 8000
   - **CPU:** 1 vCPU
   - **Memory:** 2 GB
6. **Variables de entorno:**
   ```
   SECRET_KEY = [genera con: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"]
   DEBUG = False
   ALLOWED_HOSTS = *
   DB_NAME = vpayDB
   DB_USER = postgres
   DB_PASSWORD = postgres
   DB_HOST = dbvpay.cfiek6gqkqd5.us-east-1.rds.amazonaws.com
   DB_PORT = 5432
   CORS_ALLOW_ALL_ORIGINS = True
   AWS_DEFAULT_REGION = us-east-1
   ```
7. **Instance role (IMPORTANTE):**
   - Selecciona: `CondominiumAppRunnerTaskRole`
   - ⚠️ Sin esto, Rekognition y S3 no funcionarán
8. **Health check:**
   - Path: `/health/`
   - Interval: 10s
   - Timeout: 5s
8. Click "Create & deploy"

---

### PASO 7: Verificar el despliegue

Espera 5-10 minutos. App Runner te dará una URL:
```
https://xyz123abc.us-east-1.awsapprunner.com
```

**Prueba estos endpoints:**
- ✅ Health: https://xyz123abc.us-east-1.awsapprunner.com/health/
- ✅ Swagger: https://xyz123abc.us-east-1.awsapprunner.com/api/docs/
- ✅ Admin: https://xyz123abc.us-east-1.awsapprunner.com/admin/

---

### PASO 8: Actualizaciones futuras

Cuando hagas cambios en el código:

```powershell
# Método automático
.\update-apprunner-service.ps1

# O paso a paso:
.\deploy-to-ecr.ps1  # Sube nueva imagen
# Luego en AWS Console → App Runner → Deploy
```

---

## 🛠️ HERRAMIENTAS ÚTILES

### Menu interactivo
```powershell
.\menu.ps1
```

### Comandos rápidos

```powershell
# Ver Account ID
aws sts get-caller-identity --query Account --output text

# Generar SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Ver servicios App Runner
aws apprunner list-services --region us-east-1

# Obtener URL del servicio
aws apprunner describe-service --service-arn TU_ARN --query 'Service.ServiceUrl' --output text

# Ver logs (en CloudWatch)
aws logs tail /aws/apprunner/condominium-backend-service --follow
```

---

## 📊 ESTRUCTURA DE ARCHIVOS CREADOS

```
condominium_django_be/
│
├── Dockerfile                      # Configuración Docker
├── .dockerignore                   # Archivos a excluir
├── .env.example                    # Ejemplo de variables
├── requirements.txt                # Dependencias (actualizado)
│
├── Scripts PowerShell:
├── deploy-to-ecr.ps1              # Subir a ECR
├── test-docker-local.ps1          # Probar localmente
├── create-apprunner-service.ps1   # Crear servicio
├── update-apprunner-service.ps1   # Actualizar servicio
├── menu.ps1                        # Menu interactivo
│
└── Documentación:
    ├── README_DEPLOYMENT.md        # Resumen rápido
    ├── DEPLOYMENT_GUIDE.md         # Guía detallada
    └── STEP_BY_STEP.md            # Este archivo
```

---

## ⚠️ NOTAS IMPORTANTES

### Seguridad
- ✅ Usa `DEBUG=False` en producción
- ✅ Genera SECRET_KEY única para producción
- ✅ Cambia `ALLOWED_HOSTS=*` por tu dominio real
- ✅ No subas credenciales a Git

### Base de datos
- ✅ Ya está configurada para RDS de AWS
- ⚠️ Verifica que RDS permita conexiones desde App Runner
- ⚠️ Considera configurar VPC si es necesario

### Archivos media (imágenes)
- ⚠️ Las imágenes se guardan en el contenedor (se pierden al redesplegar)
- 💡 Recomendación: Usa S3 para archivos persistentes
- 💡 Instala `django-storages` y `boto3` (ya incluidos)

### Costos aproximados
- ECR: Primeros 500MB gratis
- App Runner: ~$0.078/hora ≈ $56/mes (1 vCPU + 2GB)
- Tráfico: 100GB gratis/mes

---

## 🆘 TROUBLESHOOTING

### "Task failed to start"
- Verifica variables de entorno en App Runner
- Revisa logs en CloudWatch
- Confirma que el puerto 8000 está expuesto

### "Cannot connect to database"
- Verifica Security Group de RDS
- Asegúrate que RDS es accesible públicamente O configura VPC

### "404 Not Found"
- Verifica que ALLOWED_HOSTS incluye el dominio
- Confirma que las rutas en urls.py son correctas

### "500 Internal Server Error"
- Revisa logs en CloudWatch
- Verifica SECRET_KEY está configurada
- Confirma que DEBUG=False en producción

---

## ✅ CHECKLIST FINAL

- [ ] Imagen Docker construida y subida a ECR
- [ ] Servicio App Runner creado
- [ ] Health check responde 200 OK
- [ ] Swagger UI accesible
- [ ] SECRET_KEY guardada de forma segura
- [ ] Variables de entorno configuradas
- [ ] Logs de CloudWatch funcionando
- [ ] Base de datos conectada correctamente

---

## 🎉 ¡LISTO!

Tu backend Django está desplegado en AWS App Runner y accesible desde internet.

**Próximos pasos:**
1. Configura un dominio personalizado (Route 53)
2. Implementa CI/CD con GitHub Actions
3. Configura S3 para archivos media
4. Implementa monitoring con CloudWatch
5. Configura backups de RDS

---

¿Necesitas ayuda? Revisa:
- `DEPLOYMENT_GUIDE.md` - Guía detallada
- `README_DEPLOYMENT.md` - Resumen rápido
- AWS App Runner docs: https://docs.aws.amazon.com/apprunner/
