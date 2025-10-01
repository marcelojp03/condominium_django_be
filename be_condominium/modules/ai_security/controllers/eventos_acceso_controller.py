from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from modules.ai_security.models.access_event import AccessEvent
from modules.ai_security.models.vehicle_event import VehicleAccessEvent
from django.db.models import Q
from datetime import datetime

@api_view(['GET'])
def eventos_acceso_listar(request):
    """
    🟠 ENDPOINT FASE 2 - IMPORTANTE
    Lista historial de eventos de acceso (rostros y placas)
    Query params:
    - fecha: YYYY-MM-DD (filtro por fecha específica)
    - tipo: ROSTRO | PLACA (tipo de evento)
    - resultado: PERMITIDO | DENEGADO (si fue reconocido o no)
    - fecha_desde: YYYY-MM-DD
    - fecha_hasta: YYYY-MM-DD
    """
    fecha = request.query_params.get('fecha', None)
    tipo = request.query_params.get('tipo', None)
    resultado = request.query_params.get('resultado', None)
    fecha_desde = request.query_params.get('fecha_desde', None)
    fecha_hasta = request.query_params.get('fecha_hasta', None)
    
    eventos = []
    
    # Obtener eventos de rostros
    if not tipo or tipo == 'ROSTRO':
        rostros = AccessEvent.objects.all().select_related('matched_resident')
        
        if fecha:
            rostros = rostros.filter(timestamp__date=fecha)
        if fecha_desde:
            rostros = rostros.filter(timestamp__date__gte=fecha_desde)
        if fecha_hasta:
            rostros = rostros.filter(timestamp__date__lte=fecha_hasta)
        
        if resultado:
            if resultado == 'PERMITIDO':
                rostros = rostros.filter(matched_resident__isnull=False)
            elif resultado == 'DENEGADO':
                rostros = rostros.filter(matched_resident__isnull=True)
        
        for evento in rostros.order_by('-timestamp')[:100]:  # Limitar a 100 registros
            eventos.append({
                'id': evento.id,
                'timestamp': evento.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'tipo': 'ROSTRO',
                'resultado': 'PERMITIDO' if evento.matched_resident else 'DENEGADO',
                'residente': evento.matched_resident.name if evento.matched_resident else 'Desconocido',
                'confidence': evento.confidence,
                'imagen': request.build_absolute_uri(evento.image.url) if evento.image else None
            })
    
    # Obtener eventos de vehículos
    if not tipo or tipo == 'PLACA':
        vehiculos = VehicleAccessEvent.objects.all()
        
        if fecha:
            vehiculos = vehiculos.filter(timestamp__date=fecha)
        if fecha_desde:
            vehiculos = vehiculos.filter(timestamp__date__gte=fecha_desde)
        if fecha_hasta:
            vehiculos = vehiculos.filter(timestamp__date__lte=fecha_hasta)
        
        if resultado:
            if resultado == 'PERMITIDO':
                vehiculos = vehiculos.filter(placa_valida=True)
            elif resultado == 'DENEGADO':
                vehiculos = vehiculos.filter(placa_valida=False)
        
        for evento in vehiculos.order_by('-timestamp')[:100]:
            eventos.append({
                'id': evento.id,
                'timestamp': evento.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'tipo': 'PLACA',
                'resultado': 'PERMITIDO' if evento.placa_valida else 'DENEGADO',
                'placa': evento.plate_number or 'No detectada',
                'propietario': evento.matched_resident.name if evento.matched_resident else None,
                'confidence': evento.confidence,
                'imagen': request.build_absolute_uri(evento.image.url) if evento.image else None
            })
    
    # Ordenar por timestamp descendente
    eventos.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return Response({
        'codigo': 0,
        'mensaje': 'OK',
        'total': len(eventos),
        'eventos': eventos[:100]  # Limitar respuesta
    })

@api_view(['POST'])
def registrar_evento_manual(request):
    """
    🟡 ENDPOINT FASE 2 - IMPORTANTE
    Registro manual de eventos por guardias (visitas, deliveries, etc)
    """
    tipo = request.data.get('tipo')  # VISITA | DELIVERY | MANTENIMIENTO
    descripcion = request.data.get('descripcion', '')
    residente_id = request.data.get('residente_id')
    visitante_nombre = request.data.get('visitante_nombre', '')
    documento = request.data.get('documento', '')
    
    if not tipo:
        return Response({
            'codigo': 1,
            'mensaje': 'El campo tipo es requerido'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Buscar residente si se proporciona ID
        residente = None
        if residente_id:
            from modules.ad.models.residente_model import Residente
            residente = Residente.objects.filter(idresidente=residente_id).first()
        
        # Crear evento de acceso manual
        evento = AccessEvent.objects.create(
            matched_resident=None,  # Es manual, no hay match automático
            confidence=100.0  # Manual = 100% confianza
        )
        
        return Response({
            'codigo': 0,
            'mensaje': 'Evento registrado exitosamente',
            'evento_id': evento.id,
            'timestamp': evento.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'tipo': tipo,
            'visitante': visitante_nombre,
            'residente_destino': residente.nombres if residente else 'No especificado'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'codigo': 1,
            'mensaje': f'Error al registrar evento: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
