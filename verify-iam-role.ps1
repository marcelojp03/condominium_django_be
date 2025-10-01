# Script para verificar permisos del rol IAM existente

$ROLE_NAME = "vpay-smartdoc-apprunner-instance-role"
$AWS_ACCOUNT_ID = "851725478821"

Write-Host "🔍 Verificando permisos del rol: $ROLE_NAME" -ForegroundColor Cyan
Write-Host ""

# Verificar que el rol existe
Write-Host "=== Información del Rol ===" -ForegroundColor Green
$roleInfo = aws iam get-role --role-name $ROLE_NAME 2>$null | ConvertFrom-Json

if ($LASTEXITCODE -eq 0) {
    Write-Host "Rol encontrado" -ForegroundColor Green
    Write-Host "  ARN: $($roleInfo.Role.Arn)" -ForegroundColor White
    Write-Host "  Creado: $($roleInfo.Role.CreateDate)" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "Rol no encontrado" -ForegroundColor Red
    exit 1
}

# Ver políticas inline
Write-Host "=== Políticas Inline (Directas) ===" -ForegroundColor Green
$inlinePolicies = aws iam list-role-policies --role-name $ROLE_NAME --query 'PolicyNames' --output json | ConvertFrom-Json

if ($inlinePolicies.Count -eq 0) {
    Write-Host "  (Ninguna)" -ForegroundColor Gray
} else {
    foreach ($policyName in $inlinePolicies) {
        Write-Host "`n  📋 Política: $policyName" -ForegroundColor Yellow
        
        # Obtener documento de la política
        $policyDoc = aws iam get-role-policy `
            --role-name $ROLE_NAME `
            --policy-name $policyName `
            --query 'PolicyDocument.Statement' `
            --output json | ConvertFrom-Json
        
        foreach ($statement in $policyDoc) {
            Write-Host "    Sid: $($statement.Sid)" -ForegroundColor Cyan
            Write-Host "    Permisos:" -ForegroundColor White
            
            if ($statement.Action -is [array]) {
                foreach ($action in $statement.Action) {
                    Write-Host "      - $action" -ForegroundColor Gray
                }
            } else {
                Write-Host "      - $($statement.Action)" -ForegroundColor Gray
            }
        }
    }
}

# Ver políticas administradas adjuntas
Write-Host "`n=== Políticas Administradas (AWS Managed) ===" -ForegroundColor Green
$managedPolicies = aws iam list-attached-role-policies --role-name $ROLE_NAME --query 'AttachedPolicies' --output json | ConvertFrom-Json

if ($managedPolicies.Count -eq 0) {
    Write-Host "  (Ninguna)" -ForegroundColor Gray
} else {
    foreach ($policy in $managedPolicies) {
        Write-Host "  📌 $($policy.PolicyName)" -ForegroundColor Yellow
        Write-Host "    ARN: $($policy.PolicyArn)" -ForegroundColor Gray
    }
}

# Resumen de servicios
Write-Host "`n=== Resumen de Servicios AWS con Acceso ===" -ForegroundColor Cyan

$allActions = @()
foreach ($policyName in $inlinePolicies) {
    $policyDoc = aws iam get-role-policy `
        --role-name $ROLE_NAME `
        --policy-name $policyName `
        --query 'PolicyDocument.Statement[*].Action' `
        --output json | ConvertFrom-Json
    
    if ($policyDoc) {
        foreach ($actions in $policyDoc) {
            if ($actions -is [array]) {
                $allActions += $actions
            } else {
                $allActions += $actions
            }
        }
    }
}

$services = @{}
foreach ($action in $allActions) {
    $service = $action.Split(':')[0]
    if (-not $services.ContainsKey($service)) {
        $services[$service] = @()
    }
    $services[$service] += $action
}

foreach ($service in $services.Keys | Sort-Object) {
    $icon = switch ($service) {
        "rekognition" { "🎭" }
        "textract" { "📄" }
        "s3" { "📦" }
        "ecr" { "🐳" }
        default { "🔧" }
    }
    
    Write-Host "`n$icon $service ($($services[$service].Count) permisos)" -ForegroundColor Green
    $services[$service] | Sort-Object -Unique | ForEach-Object {
        Write-Host "  ✓ $_" -ForegroundColor Gray
    }
}

# Verificar permisos necesarios para Condominio
Write-Host "`n=== Verificación para Condominium Backend ===" -ForegroundColor Cyan

$requiredPermissions = @{
    "Rekognition" = @("rekognition:DetectFaces", "rekognition:IndexFaces", "rekognition:SearchFacesByImage", "rekognition:DetectText", "rekognition:DetectCustomLabels")
    "Textract" = @("textract:DetectDocumentText", "textract:AnalyzeDocument")
    "S3" = @("s3:GetObject", "s3:PutObject", "s3:DeleteObject")
}

foreach ($service in $requiredPermissions.Keys) {
    Write-Host "`n${service}:" -ForegroundColor Yellow
    foreach ($perm in $requiredPermissions[$service]) {
        if ($allActions -contains $perm) {
            Write-Host "  ✅ $perm" -ForegroundColor Green
        } else {
            Write-Host "  ❌ $perm (FALTANTE)" -ForegroundColor Red
        }
    }
}

Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📝 RECOMENDACIONES:" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

$missingPerms = @()
foreach ($service in $requiredPermissions.Keys) {
    foreach ($perm in $requiredPermissions[$service]) {
        if ($allActions -notcontains $perm) {
            $missingPerms += $perm
        }
    }
}

if ($missingPerms.Count -gt 0) {
    Write-Host "`n⚠️ Permisos faltantes detectados:" -ForegroundColor Yellow
    $missingPerms | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
    Write-Host "`nEjecuta: .\setup-iam.ps1 para agregar los permisos faltantes" -ForegroundColor Cyan
} else {
    Write-Host "`n✅ Todos los permisos necesarios están presentes!" -ForegroundColor Green
    Write-Host "Tu rol está listo para usarse con Condominium Backend" -ForegroundColor White
}

Write-Host ""
