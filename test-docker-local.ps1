# Test local de la imagen Docker antes de subirla a AWS

Write-Host "=== Construyendo imagen Docker ===" -ForegroundColor Green
docker build -t condominium-backend:test .

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n=== Imagen construida exitosamente ===" -ForegroundColor Green
    Write-Host "`nPara probar localmente, ejecuta:" -ForegroundColor Yellow
    Write-Host "docker run -p 8000:8000 -e DEBUG=True condominium-backend:test" -ForegroundColor Cyan
    Write-Host "`nLuego accede a: http://localhost:8000/api/docs/" -ForegroundColor Cyan
} else {
    Write-Host "`n=== Error al construir la imagen ===" -ForegroundColor Red
    exit 1
}
