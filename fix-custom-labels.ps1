# Script rápido para agregar DetectCustomLabels

$ROLE_NAME = "vpay-smartdoc-apprunner-instance-role"
$POLICY_NAME = "CondominiumAdditionalPermissions"

Write-Host "🔧 Actualizando política con DetectCustomLabels..." -ForegroundColor Cyan

$updatedPolicy = @"
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "S3Permissions",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:PutObjectAcl",
                "s3:DeleteObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::*/*",
                "arn:aws:s3:::*"
            ]
        },
        {
            "Sid": "RekognitionAdditional",
            "Effect": "Allow",
            "Action": [
                "rekognition:DetectFaces",
                "rekognition:IndexFaces",
                "rekognition:SearchFaces",
                "rekognition:SearchFacesByImage",
                "rekognition:DetectLabels",
                "rekognition:DetectCustomLabels",
                "rekognition:CompareFaces",
                "rekognition:ListCollections",
                "rekognition:ListFaces",
                "rekognition:DeleteFaces"
            ],
            "Resource": "*"
        }
    ]
}
"@

$updatedPolicy | Out-File -FilePath "temp-updated-policy.json" -Encoding UTF8 -NoNewline

aws iam put-role-policy `
    --role-name $ROLE_NAME `
    --policy-name $POLICY_NAME `
    --policy-document file://temp-updated-policy.json

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Política actualizada con DetectCustomLabels" -ForegroundColor Green
} else {
    Write-Host "❌ Error al actualizar la política" -ForegroundColor Red
}

Remove-Item "temp-updated-policy.json" -ErrorAction SilentlyContinue

Write-Host "`nVerificando cambios..." -ForegroundColor Yellow
.\verify-iam-role.ps1
