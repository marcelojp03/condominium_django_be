from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from modules.cn.models.cuota_model import Cuota
from modules.ad.models.residente_model import Residente
from modules.ad.models.reserva_area_model import ReservaArea
from modules.ad.models.aviso_model import Aviso
from modules.ad.models.unidad_model import Unidad
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta, datetime

@api_view(['GET'])
def dashboard_residente(request, residente_id):
    """
    🟢 ENDPOINT FASE 3 - OPCIONAL
    Dashboard con estadísticas del residente
    """
    try:
        residente = Residente.objects.filter(idresidente=residente_id).first()
        if not residente:
            return Response({
                'codigo': 1,
                'mensaje': 'Residente no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Obtener unidades del residente
        unidades_ids = [residente.unidad.idunidad]
        
        # Cuotas pendientes
        cuotas_pendientes = Cuota.objects.filter(
            unidad_id__in=unidades_ids,
            estado_pago='PENDIENTE'
        )
        
        # Monto total pendiente
        monto_pendiente = cuotas_pendientes.aggregate(
            total=Sum('monto')
        )['total'] or 0
        
        # Próxima cuota a vencer
        proxima_cuota = cuotas_pendientes.order_by('periodo').first()
        proxima_vence = proxima_cuota.periodo if proxima_cuota else None
        
        # Reservas activas (futuras)
        hoy = timezone.now().date()
        reservas_activas = ReservaArea.objects.filter(
            residente_id=residente_id,
            fecha_reserva__gte=hoy,
            estado=True
        ).count()
        
        # Avisos sin leer (todos los avisos vigentes)
        avisos_vigentes = Aviso.objects.filter(
            vigente_hasta__gte=hoy,
            estado=True
        ).count()
        
        # Estadísticas de pagos (últimos 6 meses)
        seis_meses_atras = timezone.now() - timedelta(days=180)
        cuotas_pagadas = Cuota.objects.filter(
            unidad_id__in=unidades_ids,
            estado_pago='PAGADO',
            fecha_pago__gte=seis_meses_atras
        ).count()
        
        monto_pagado_6meses = Cuota.objects.filter(
            unidad_id__in=unidades_ids,
            estado_pago='PAGADO',
            fecha_pago__gte=seis_meses_atras
        ).aggregate(total=Sum('monto'))['total'] or 0
        
        dashboard = {
            'residente': {
                'id': residente.idresidente,
                'nombre': f"{residente.nombres} {residente.apellido1}",
                'unidad': residente.unidad.codigo
            },
            'cuotas_pendientes': cuotas_pendientes.count(),
            'monto_total_pendiente': float(monto_pendiente),
            'proxima_cuota_vence': proxima_vence,
            'reservas_activas': reservas_activas,
            'avisos_sin_leer': avisos_vigentes,
            'estadisticas_6meses': {
                'pagos_realizados': cuotas_pagadas,
                'monto_pagado': float(monto_pagado_6meses)
            },
            'fecha_consulta': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return Response({
            'codigo': 0,
            'mensaje': 'OK',
            'dashboard': dashboard
        })
        
    except Exception as e:
        return Response({
            'codigo': 1,
            'mensaje': f'Error al generar dashboard: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def dashboard_guardia(request):
    """
    🟢 ENDPOINT FASE 3 - OPCIONAL
    Dashboard con estadísticas para guardias
    """
    try:
        from modules.ai_security.models.access_event import AccessEvent
        from modules.ai_security.models.vehicle_event import VehicleAccessEvent
        
        hoy = timezone.now().date()
        
        # Accesos de hoy (rostros)
        accesos_rostro_hoy = AccessEvent.objects.filter(
            timestamp__date=hoy
        ).count()
        
        # Visitantes permitidos hoy
        visitantes_permitidos = AccessEvent.objects.filter(
            timestamp__date=hoy,
            matched_resident__isnull=False
        ).count()
        
        # Intentos denegados
        intentos_denegados = AccessEvent.objects.filter(
            timestamp__date=hoy,
            matched_resident__isnull=True
        ).count()
        
        # Vehículos ingresados hoy
        vehiculos_hoy = VehicleAccessEvent.objects.filter(
            timestamp__date=hoy
        ).count()
        
        # Eventos sospechosos pendientes
        from modules.ai_security.models.evento_sospechoso import EventoSospechoso
        alertas_pendientes = EventoSospechoso.objects.filter(
            fecha_hora__date=hoy
        ).count()
        
        # Última actividad
        ultimo_evento = AccessEvent.objects.order_by('-timestamp').first()
        ultima_actividad = ultimo_evento.timestamp.strftime('%Y-%m-%d %H:%M:%S') if ultimo_evento else 'Sin actividad'
        
        dashboard = {
            'fecha': hoy.strftime('%Y-%m-%d'),
            'accesos_hoy': accesos_rostro_hoy,
            'visitantes_permitidos': visitantes_permitidos,
            'intentos_denegados': intentos_denegados,
            'vehiculos_ingresados': vehiculos_hoy,
            'alertas_pendientes': alertas_pendientes,
            'ultima_actividad': ultima_actividad,
            'resumen_turno': {
                'total_eventos': accesos_rostro_hoy + vehiculos_hoy,
                'tasa_reconocimiento': round((visitantes_permitidos / accesos_rostro_hoy * 100), 2) if accesos_rostro_hoy > 0 else 0
            }
        }
        
        return Response({
            'codigo': 0,
            'mensaje': 'OK',
            'dashboard': dashboard
        })
        
    except Exception as e:
        return Response({
            'codigo': 1,
            'mensaje': f'Error al generar dashboard: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
