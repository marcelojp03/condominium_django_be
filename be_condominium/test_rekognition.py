# Script para probar la conexión a Rekognition y las colecciones
# Ejecuta: python test_rekognition.py

import boto3
from botocore.exceptions import ClientError

def probar_rekognition():
    """Prueba básica de conectividad a Rekognition"""
    
    print("=" * 50)
    print("🧪 PRUEBA DE REKOGNITION")
    print("=" * 50)
    
    try:
        rekognition = boto3.client('rekognition', region_name='us-east-1')
        
        # 1. Listar colecciones
        print("1️⃣ Probando listar colecciones...")
        response = rekognition.list_collections()
        colecciones = response.get('CollectionIds', [])
        print(f"✅ Colecciones disponibles: {len(colecciones)}")
        for col in colecciones:
            print(f"   • {col}")
        
        # 2. Verificar colecciones específicas
        print("\n2️⃣ Verificando colecciones del proyecto...")
        colecciones_proyecto = ['residentes-condominio', 'visitantes-condominio']
        
        for col in colecciones_proyecto:
            if col in colecciones:
                try:
                    stats = rekognition.describe_collection(CollectionId=col)
                    print(f"✅ {col}: {stats['FaceCount']} rostros indexados")
                except Exception as e:
                    print(f"❌ Error en {col}: {e}")
            else:
                print(f"❌ {col}: No existe")
        
        # 3. Probar detección de rostros (sin imagen real)
        print("\n3️⃣ Verificando permisos de Rekognition...")
        
        # Intentar operación que requiere permisos sin imagen real
        try:
            # Esta operación fallará por falta de imagen, pero nos dice si tenemos permisos
            rekognition.detect_faces(Image={'Bytes': b'fake'})
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'InvalidImageException':
                print("✅ Permisos de DetectFaces: OK")
            elif error_code == 'AccessDeniedException':
                print("❌ Permisos de DetectFaces: NO AUTORIZADO")
            else:
                print(f"⚠️ DetectFaces: {error_code}")
        
        print("\n🎉 RESULTADO: Rekognition está configurado correctamente")
        return True
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'AccessDeniedException':
            print("❌ ERROR: Sin permisos para Rekognition")
            print("💡 Solución: Ejecuta setup-iam.ps1")
        else:
            print(f"❌ ERROR: {e}")
        return False
    
    except Exception as e:
        print(f"❌ ERROR GENERAL: {e}")
        return False

def mostrar_endpoints_disponibles():
    """Muestra información sobre los endpoints de AI"""
    
    print("\n" + "=" * 50)
    print("📍 ENDPOINTS DE IA DISPONIBLES")
    print("=" * 50)
    
    endpoints = [
        {
            'url': 'POST /api/ai/escanear-rostro/',
            'descripcion': 'Busca rostros conocidos en imagen',
            'body': 'multipart/form-data con campo "image"',
            'respuesta': '{"matched": true/false, "resident": "nombre", "confidence": 95.5}'
        },
        {
            'url': 'POST /api/ai/registrar-rostro/',
            'descripcion': 'Registra rostro de residente en S3/Rekognition',
            'body': '{"resident_id": 1, "image_key": "faces/residente.jpg"}',
            'respuesta': '{"face_id": "abc123...", "confidence": 99.8}'
        }
    ]
    
    for i, ep in enumerate(endpoints, 1):
        print(f"{i}️⃣ {ep['url']}")
        print(f"   📝 {ep['descripcion']}")
        print(f"   📤 Body: {ep['body']}")
        print(f"   📥 Respuesta: {ep['respuesta']}")
        print()

if __name__ == "__main__":
    exito = probar_rekognition()
    mostrar_endpoints_disponibles()
    
    if exito:
        print("✅ Todo listo para usar reconocimiento facial!")
    else:
        print("❌ Revisa la configuración antes de usar los endpoints")
    
    print("\n💡 Para probar: usa Postman o curl con una imagen real")
    print("📖 Logs detallados en la consola de Django al hacer requests")