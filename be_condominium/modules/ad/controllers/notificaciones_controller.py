from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

@api_view(['POST'])
def enviar_notificacion_push(request):
    """
    🟡 ENDPOINT FASE 3 - OPCIONAL
    Sistema de notificaciones push (simulado - integrar con Firebase/OneSignal después)
    Body:
    - destinatarios: array ['GUARDIAS', 'RESIDENTES', 'ADMIN']
    - titulo: string
    - mensaje: string
    - tipo: 'URGENTE' | 'INFO' | 'ALERTA'
    """
    destinatarios = request.data.get('destinatarios', [])
    titulo = request.data.get('titulo', '')
    mensaje = request.data.get('mensaje', '')
    tipo = request.data.get('tipo', 'INFO')
    
    if not destinatarios or not titulo or not mensaje:
        return Response({
            'codigo': 1,
            'mensaje': 'destinatarios, titulo y mensaje son requeridos'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # SIMULACIÓN - En producción integrar con:
        # - Firebase Cloud Messaging (FCM)
        # - OneSignal
        # - Amazon SNS
        
        # Por ahora solo registramos el intento
        notificacion_log = {
            'timestamp': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            'destinatarios': destinatarios,
            'titulo': titulo,
            'mensaje': mensaje,
            'tipo': tipo,
            'enviada': True,
            'plataforma': 'SIMULADO'  # Cambiar a 'FCM' o 'OneSignal' en producción
        }
        
        # Calcular cantidad estimada de destinatarios
        from modules.ad.models.usuario import Usuario
        cantidad_destinatarios = 0
        
        for perfil in destinatarios:
            if perfil == 'GUARDIAS':
                # Contar usuarios con rol guardia
                cantidad_destinatarios += Usuario.objects.filter(
                    roles__nombre__icontains='guardia',
                    activo=True
                ).count()
            elif perfil == 'RESIDENTES':
                # Contar usuarios con rol residente
                cantidad_destinatarios += Usuario.objects.filter(
                    roles__nombre__icontains='residente',
                    activo=True
                ).count()
            elif perfil == 'ADMIN':
                # Contar administradores
                cantidad_destinatarios += Usuario.objects.filter(
                    roles__nombre__icontains='admin',
                    activo=True
                ).count()
        
        return Response({
            'codigo': 0,
            'mensaje': 'Notificación enviada exitosamente (simulado)',
            'notificacion': {
                'id': f"NOTIF-{timezone.now().timestamp()}",
                'timestamp': notificacion_log['timestamp'],
                'destinatarios': destinatarios,
                'cantidad_usuarios': cantidad_destinatarios,
                'titulo': titulo,
                'tipo': tipo,
                'estado': 'ENVIADA',
                'nota': 'Sistema simulado - Integrar con FCM/OneSignal para producción'
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'codigo': 1,
            'mensaje': f'Error al enviar notificación: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def registrar_token_dispositivo(request):
    """
    🟢 ENDPOINT ADICIONAL
    Registrar token FCM del dispositivo móvil para notificaciones
    """
    usuario_id = request.data.get('usuario_id')
    token = request.data.get('token')
    plataforma = request.data.get('plataforma', 'android')  # android | ios
    
    if not usuario_id or not token:
        return Response({
            'codigo': 1,
            'mensaje': 'usuario_id y token son requeridos'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Aquí guardarías el token en una tabla DeviceTokens
        # Por ahora solo simulamos
        
        return Response({
            'codigo': 0,
            'mensaje': 'Token registrado exitosamente',
            'usuario_id': usuario_id,
            'plataforma': plataforma,
            'nota': 'Implementar tabla DeviceTokens para producción'
        })
        
    except Exception as e:
        return Response({
            'codigo': 1,
            'mensaje': f'Error al registrar token: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
