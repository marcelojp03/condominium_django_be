from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from modules.cn.services.cuota_service import CuotaService
from modules.cn.dtos.cuota_dto import CuotaSerializer
from django.utils import timezone

@api_view(['GET'])
def cuota_listar(request):
    # 🔴 FILTRO POR RESIDENTE - CRÍTICO PARA APP MÓVIL
    residente_id = request.query_params.get('residente_id', None)
    estado = request.query_params.get('estado', None)
    fecha_desde = request.query_params.get('fecha_desde', None)
    fecha_hasta = request.query_params.get('fecha_hasta', None)
    
    cuotas = CuotaService.listar_cuotas(
        residente_id=residente_id,
        estado=estado,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta
    )
    serializer = CuotaSerializer(cuotas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def cuota_detalle(request, idcuota):
    cuota = CuotaService.obtener_cuota(idcuota)
    if cuota:
        serializer = CuotaSerializer(cuota)
        return Response(serializer.data)
    return Response({'error': 'Cuota no encontrada'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def cuota_crear(request):
    serializer = CuotaSerializer(data=request.data)
    if serializer.is_valid():
        CuotaService.crear_cuota(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def cuota_actualizar(request, idcuota):
    serializer = CuotaSerializer(data=request.data)
    if serializer.is_valid():
        CuotaService.actualizar_cuota(idcuota, serializer.validated_data)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def cuota_eliminar(request, idcuota):
    CuotaService.eliminar_cuota(idcuota)
    return Response({'mensaje': 'Cuota anulada'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def cuota_pagar(request, idcuota):
    """
    🔴 ENDPOINT CRÍTICO - PAGAR CUOTA
    Registra el pago de una cuota con comprobante
    Body: {
        'forma_pago_id': int,
        'monto': decimal,
        'comprobante': str (opcional - URL o base64)
    }
    """
    forma_pago_id = request.data.get('forma_pago_id')
    monto = request.data.get('monto')
    comprobante = request.data.get('comprobante', '')
    
    if not forma_pago_id or not monto:
        return Response({
            'codigo': 1,
            'mensaje': 'Forma de pago y monto son requeridos'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        cuota = CuotaService.pagar_cuota(
            idcuota=idcuota,
            forma_pago_id=forma_pago_id,
            monto=monto,
            comprobante=comprobante
        )
        
        if cuota:
            return Response({
                'codigo': 0,
                'mensaje': 'Pago registrado exitosamente',
                'cuota_id': cuota.idcuota,
                'estado': cuota.estado_pago,
                'fecha_pago': cuota.fecha_pago
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'codigo': 1,
                'mensaje': 'Cuota no encontrada'
            }, status=status.HTTP_404_NOT_FOUND)
            
    except Exception as e:
        return Response({
            'codigo': 1,
            'mensaje': f'Error al procesar pago: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
