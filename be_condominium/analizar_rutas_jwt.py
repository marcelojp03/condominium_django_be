# Script para analizar qué rutas requieren JWT
# Ejecuta: python analizar_rutas_jwt.py

import os
import re
from pathlib import Path

def analizar_permisos_en_archivo(archivo_path):
    """Analiza un archivo de controller y extrae información de permisos"""
    try:
        with open(archivo_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Buscar funciones de vista con decoradores
        patron_funcion = r'@api_view\([^\)]+\)\s*(?:@permission_classes\(([^\)]+)\))?\s*def\s+(\w+)'
        matches = re.findall(patron_funcion, contenido, re.MULTILINE | re.DOTALL)
        
        funciones = []
        for match in matches:
            permisos = match[0].strip() if match[0] else None
            nombre_funcion = match[1]
            
            # Determinar el tipo de permiso
            if permisos and 'AllowAny' in permisos:
                tipo_permiso = "🟢 PÚBLICO (AllowAny)"
            elif permisos and 'IsAuthenticated' in permisos:
                tipo_permiso = "🔒 REQUIERE JWT (IsAuthenticated)"
            elif permisos is None:
                tipo_permiso = "🔒 REQUIERE JWT (Default: IsAuthenticated)"
            else:
                tipo_permiso = f"⚠️ PERSONALIZADO ({permisos})"
            
            funciones.append({
                'nombre': nombre_funcion,
                'permiso': tipo_permiso,
                'decorador': permisos or "Sin @permission_classes (usa default)"
            })
        
        return funciones
    except Exception as e:
        return [{'error': str(e)}]

def obtener_rutas_desde_urls(urls_path, modulo_nombre):
    """Extrae las rutas definidas en urls.py"""
    try:
        with open(urls_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Buscar patrones path('ruta/', controller.funcion)
        patron_path = r"path\(['\"]([^'\"]+)['\"],\s*(\w+)\.(\w+)"
        matches = re.findall(patron_path, contenido)
        
        rutas = []
        for match in matches:
            ruta = match[0]
            controller = match[1]
            funcion = match[2]
            
            rutas.append({
                'url': f"/{modulo_nombre}/{ruta}",
                'controller': controller,
                'funcion': funcion
            })
        
        return rutas
    except Exception as e:
        return [{'error': str(e)}]

def main():
    print("=" * 60)
    print("🔍 ANÁLISIS DE AUTENTICACIÓN JWT EN RUTAS")
    print("=" * 60)
    print()
    
    # Configuración actual
    print("📋 CONFIGURACIÓN ACTUAL:")
    print("   • DEFAULT_PERMISSION_CLASSES = ['rest_framework.permissions.IsAuthenticated']")
    print("   • DEFAULT_AUTHENTICATION_CLASSES incluye JWTAuthentication")
    print("   • Por defecto: TODAS las rutas requieren JWT")
    print("   • Excepción: Rutas con @permission_classes([AllowAny])")
    print()
    
    base_path = Path("modules")
    modulos = []
    
    # Analizar cada módulo
    for modulo_dir in base_path.iterdir():
        if modulo_dir.is_dir() and (modulo_dir / "urls.py").exists():
            modulo_nombre = modulo_dir.name
            urls_path = modulo_dir / "urls.py"
            controllers_path = modulo_dir / "controllers"
            
            print(f"📁 MÓDULO: {modulo_nombre.upper()}")
            print("-" * 40)
            
            # Obtener rutas
            rutas = obtener_rutas_desde_urls(urls_path, modulo_nombre)
            
            # Analizar controllers
            permisos_por_funcion = {}
            if controllers_path.exists():
                for controller_file in controllers_path.glob("*.py"):
                    if controller_file.name != "__init__.py":
                        funciones = analizar_permisos_en_archivo(controller_file)
                        for func in funciones:
                            if 'error' not in func:
                                permisos_por_funcion[func['nombre']] = func['permiso']
            
            # Mostrar resultados combinados
            for ruta in rutas:
                if 'error' not in ruta:
                    funcion_nombre = ruta['funcion']
                    permiso = permisos_por_funcion.get(funcion_nombre, "🔒 REQUIERE JWT (Default)")
                    
                    print(f"   {permiso}")
                    print(f"   └── {ruta['url']}")
                    print(f"       Controller: {ruta['controller']}.{ruta['funcion']}")
                    print()
            
            print()
    
    print("=" * 60)
    print("📖 LEYENDA:")
    print("🟢 PÚBLICO      = No requiere token JWT (acceso libre)")
    print("🔒 REQUIERE JWT = Necesita header: Authorization: Bearer <token>")
    print("⚠️ PERSONALIZADO = Permisos específicos definidos")
    print()
    
    print("💡 CÓMO USAR JWT:")
    print("1. Hacer login: POST /ad/auth/login")
    print("2. Copiar el 'token' de la respuesta")
    print("3. En Postman: Authorization > Bearer Token > pegar token")
    print("4. Para rutas 🔒, usar el token. Para rutas 🟢, no necesario.")
    print()

if __name__ == "__main__":
    main()