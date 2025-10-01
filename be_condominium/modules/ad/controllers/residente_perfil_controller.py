from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from modules.ad.models.residente_model import Residente
from modules.ad.models.usuario import Usuario
from modules.ad.models.vehiculo_model import Vehiculo

@api_view(['GET'])
def residente_mis_datos(request, usuario_id):
    """
    🟡 ENDPOINT FASE 2 - IMPORTANTE
    Obtiene el perfil completo del residente vinculado a un usuario
    Incluye: datos personales, unidad, vehículos registrados
    """
    try:
        # Buscar usuario
        usuario = Usuario.objects.filter(idusuario=usuario_id).first()
        if not usuario:
            return Response({
                'codigo': 1,
                'mensaje': 'Usuario no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Buscar residente por correo electrónico
        residente = Residente.objects.filter(
            correo_electronico=usuario.correo,
            estado=True
        ).select_related('unidad', 'tipo_documento').first()
        
        if not residente:
            return Response({
                'codigo': 1,
                'mensaje': 'No se encontró residente vinculado a este usuario'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Obtener vehículos del residente
        vehiculos = Vehiculo.objects.filter(
            residente=residente,
            estado=True
        ).values('idvehiculo', 'placa', 'marca', 'modelo', 'color', 'anio')
        
        # Obtener información de la unidad
        unidad_info = {
            'id': residente.unidad.idunidad,
            'codigo': residente.unidad.codigo,
            'piso': residente.unidad.piso,
            'numero': residente.unidad.numero,
            'direccion': f"{residente.unidad.codigo} - Piso {residente.unidad.piso}"
        }
        
        # Construir respuesta completa
        perfil = {
            'residente_id': residente.idresidente,
            'usuario_id': usuario.idusuario,
            'nombres': residente.nombres,
            'apellidos': f"{residente.apellido1} {residente.apellido2}",
            'nombre_completo': f"{residente.nombres} {residente.apellido1} {residente.apellido2}",
            'documento': {
                'tipo': residente.tipo_documento.nombre if residente.tipo_documento else 'N/A',
                'numero': residente.numero_documento,
                'extension': residente.extension_documento or ''
            },
            'correo': residente.correo_electronico,
            'unidad': unidad_info,
            'relacion': residente.relacion,
            'vehiculos': list(vehiculos),
            'fecha_registro': residente.fecha_alta.strftime('%Y-%m-%d'),
            'usuario': {
                'id': usuario.idusuario,
                'nombre': usuario.nombre,
                'correo': usuario.correo,
                'activo': usuario.activo
            }
        }
        
        return Response({
            'codigo': 0,
            'mensaje': 'OK',
            'perfil': perfil
        })
        
    except Exception as e:
        return Response({
            'codigo': 1,
            'mensaje': f'Error al obtener perfil: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
