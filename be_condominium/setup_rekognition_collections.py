# Script para configurar las colecciones de Rekognition
# Ejecuta: python setup_rekognition_collections.py

import boto3
import json
from botocore.exceptions import ClientError

def verificar_y_crear_colecciones():
    """Verifica y crea las colecciones necesarias para Rekognition"""
    
    rekognition = boto3.client('rekognition', region_name='us-east-1')
    
    # Colecciones que necesita tu aplicación
    colecciones_necesarias = [
        'residentes-condominio',
        'visitantes-condominio'
    ]
    
    print("=" * 60)
    print("🔍 CONFIGURACIÓN DE COLECCIONES REKOGNITION")
    print("=" * 60)
    print()
    
    try:
        # Listar colecciones existentes
        print("📋 Verificando colecciones existentes...")
        response = rekognition.list_collections()
        colecciones_existentes = response.get('CollectionIds', [])
        
        print(f"✅ Colecciones encontradas: {len(colecciones_existentes)}")
        for coleccion in colecciones_existentes:
            print(f"   • {coleccion}")
        print()
        
        # Crear colecciones faltantes
        for coleccion in colecciones_necesarias:
            if coleccion not in colecciones_existentes:
                print(f"🔧 Creando colección: {coleccion}")
                try:
                    rekognition.create_collection(CollectionId=coleccion)
                    print(f"✅ Colección '{coleccion}' creada exitosamente")
                except ClientError as e:
                    error_code = e.response['Error']['Code']
                    if error_code == 'ResourceAlreadyExistsException':
                        print(f"⚠️ Colección '{coleccion}' ya existe")
                    else:
                        print(f"❌ Error creando '{coleccion}': {e}")
            else:
                print(f"✅ Colección '{coleccion}' ya existe")
        
        print()
        print("=" * 60)
        print("📊 RESUMEN FINAL")
        print("=" * 60)
        
        # Verificar colecciones finales
        response = rekognition.list_collections()
        colecciones_finales = response.get('CollectionIds', [])
        
        for coleccion in colecciones_necesarias:
            if coleccion in colecciones_finales:
                print(f"✅ {coleccion} - DISPONIBLE")
                
                # Obtener estadísticas de la colección
                try:
                    stats = rekognition.describe_collection(CollectionId=coleccion)
                    face_count = stats['FaceCount']
                    print(f"   └── Rostros indexados: {face_count}")
                except Exception as e:
                    print(f"   └── Error obteniendo stats: {e}")
            else:
                print(f"❌ {coleccion} - NO DISPONIBLE")
        
        print()
        print("💡 NOTAS IMPORTANTES:")
        print("• Las colecciones están vacías inicialmente")
        print("• Los rostros se indexan cuando subes fotos de residentes")
        print("• La búsqueda funciona solo después de indexar rostros")
        print("• Costo: ~$1 USD por 1000 rostros indexados")
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'AccessDeniedException':
            print("❌ ERROR: No tienes permisos para acceder a Rekognition")
            print("💡 Solución: Ejecuta el script setup-iam.ps1 para configurar permisos")
        else:
            print(f"❌ ERROR: {e}")
    except Exception as e:
        print(f"❌ ERROR INESPERADO: {e}")

def verificar_project_arn():
    """Verifica el ARN del proyecto de Custom Labels"""
    
    print()
    print("=" * 60)
    print("🎯 VERIFICACIÓN DE CUSTOM LABELS PROJECT")
    print("=" * 60)
    
    rekognition = boto3.client('rekognition', region_name='us-east-1')
    project_arn = 'arn:aws:rekognition:us-east-1:851725478821:project/ComportamientoSospechoso/version/ComportamientoSospechoso.2025-09-21T20.10.36/1758499835614'
    
    try:
        # Verificar el proyecto
        response = rekognition.describe_project_versions(
            ProjectArn='arn:aws:rekognition:us-east-1:851725478821:project/ComportamientoSospechoso'
        )
        
        print(f"✅ Proyecto encontrado: ComportamientoSospechoso")
        
        for version in response['ProjectVersionDescriptions']:
            version_arn = version['ProjectVersionArn']
            status = version['Status']
            print(f"   • Versión: {version_arn.split('/')[-2]}")
            print(f"     Estado: {status}")
            
            if version_arn == project_arn:
                print(f"     ✅ ARN coincide con tu código")
            else:
                print(f"     ⚠️ ARN diferente en tu código")
    
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'ResourceNotFoundException':
            print("❌ Proyecto 'ComportamientoSospechoso' no encontrado")
            print("💡 Puede que necesites crear el proyecto en la consola de AWS")
        else:
            print(f"❌ Error verificando proyecto: {e}")

if __name__ == "__main__":
    verificar_y_crear_colecciones()
    verificar_project_arn()
    
    print()
    print("🚀 ¡Configuración completada!")
    print("📖 Ahora puedes usar las funciones de reconocimiento facial")
    print()