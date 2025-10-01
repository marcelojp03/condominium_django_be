# Resumen de despliegue en AWS

## 📦 Archivos creados:

1. **Dockerfile** - Configuración de la imagen Docker
2. **.dockerignore** - Archivos a excluir de la imagen
3. **.env.example** - Ejemplo de variables de entorno
4. **deploy-to-ecr.ps1** - Script para subir a AWS ECR
5. **test-docker-local.ps1** - Script para probar localmente
6. **menu.ps1** - Menu interactivo con comandos útiles
7. **DEPLOYMENT_GUIDE.md** - Guía detallada de despliegue

## 🚀 Pasos rápidos:

### 1. Probar localmente (opcional)
```powershell
.\test-docker-local.ps1
```

### 2. Configurar AWS
```powershell
aws configure
# Ingresa tus credenciales
```

### 3. Modificar deploy-to-ecr.ps1
Edita estas líneas:
```powershell
$AWS_ACCOUNT_ID = "TU_ACCOUNT_ID"  # Obtén con: aws sts get-caller-identity
$AWS_REGION = "us-east-1"
```

### 4. Desplegar
```powershell
.\deploy-to-ecr.ps1
```

### 5. Crear servicio en App Runner
Ve a: https://console.aws.amazon.com/apprunner/
- Container registry → Amazon ECR
- Selecciona: condominium-backend:latest
- Port: 8000
- Variables de entorno (importante):
  ```
  SECRET_KEY=genera-una-nueva-con-el-menu
  DEBUG=False
  ALLOWED_HOSTS=*
  ```

### 6. Health check configurado
Tu aplicación responde en: `/health/`

## 📝 URLs disponibles en producción:

- Health Check: `https://tu-app.awsapprunner.com/health/`
- API Docs: `https://tu-app.awsapprunner.com/api/docs/`
- Admin: `https://tu-app.awsapprunner.com/admin/`

## 🔧 Menu interactivo:

Para acceso rápido a todos los comandos:
```powershell
.\menu.ps1
```

## ⚠️ Notas importantes:

1. **SECRET_KEY**: Genera una nueva para producción (usa el menu, opción 5)
2. **ALLOWED_HOSTS**: En producción, cambia `*` por tu dominio real
3. **DEBUG**: Debe ser `False` en producción
4. **Base de datos**: Ya está configurada para AWS RDS
5. **Archivos media**: Considera usar S3 para imágenes en producción

## 💰 Costos estimados:

- App Runner: ~$56/mes (1 vCPU + 2GB, uso continuo)
- ECR: Primeros 500MB gratis, luego ~$0.10/GB/mes
- RDS: Según tu instancia actual

## 🆘 Soporte:

- Lee DEPLOYMENT_GUIDE.md para más detalles
- Usa menu.ps1 para comandos rápidos
- Revisa logs en CloudWatch si hay problemas
