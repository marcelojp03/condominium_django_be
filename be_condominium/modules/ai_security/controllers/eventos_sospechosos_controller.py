from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from modules.ai_security.models.evento_sospechoso import EventoSospechoso
from django.utils import timezone

@api_view(['GET'])
def eventos_sospechosos_listar(request):
    """
    🟡 ENDPOINT FASE 3 - OPCIONAL
    Lista eventos sospechosos detectados por IA
    Query params:
    - fecha_desde: YYYY-MM-DD
    - atendido: true | false
    """
    fecha_desde = request.query_params.get('fecha_desde', None)
    atendido = request.query_params.get('atendido', None)
    
    queryset = EventoSospechoso.objects.all()
    
    if fecha_desde:
        queryset = queryset.filter(fecha_hora__date__gte=fecha_desde)
    
    # Por ahora todos son no atendidos (agregar campo en modelo después)
    eventos = []
    for evento in queryset.order_by('-fecha_hora')[:50]:
        eventos.append({
            'id': evento.id,
            'timestamp': evento.fecha_hora.strftime('%Y-%m-%d %H:%M:%S'),
            'tipo_comportamiento': evento.tipo_evento,
            'confidence': evento.confianza,
            'ubicacion': 'Entrada principal',  # Default
            'imagen': request.build_absolute_uri(evento.imagen.url) if evento.imagen else None,
            'atendido': False,  # Agregar campo después
            'metadatos': evento.metadatos
        })
    
    return Response({
        'codigo': 0,
        'mensaje': 'OK',
        'total': len(eventos),
        'eventos': eventos
    })

@api_view(['PUT'])
def evento_sospechoso_atender(request, id):
    """
    🟡 ENDPOINT FASE 3 - OPCIONAL
    Marcar evento sospechoso como atendido
    """
    guardia_id = request.data.get('guardia_id')
    observaciones = request.data.get('observaciones', '')
    
    try:
        evento = EventoSospechoso.objects.filter(id=id).first()
        if not evento:
            return Response({
                'codigo': 1,
                'mensaje': 'Evento no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Actualizar metadatos con información de atención
        evento.metadatos['atendido'] = True
        evento.metadatos['guardia_id'] = guardia_id
        evento.metadatos['observaciones'] = observaciones
        evento.metadatos['fecha_atencion'] = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        evento.save()
        
        return Response({
            'codigo': 0,
            'mensaje': 'Evento marcado como atendido',
            'evento_id': evento.id
        })
        
    except Exception as e:
        return Response({
            'codigo': 1,
            'mensaje': f'Error al actualizar evento: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
