from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from modules.ad.services.reserva_area_service import ReservaAreaService
from modules.ad.dtos.reserva_area_dto import ReservaAreaSerializer

@api_view(['GET'])
def reserva_area_listar(request):
    # 🔴 FILTRO POR RESIDENTE - CRÍTICO PARA APP MÓVIL
    residente_id = request.query_params.get('residente_id', None)
    estado = request.query_params.get('estado', None)
    
    reservas = ReservaAreaService.listar_reservas(
        residente_id=residente_id,
        estado=estado
    )
    serializer = ReservaAreaSerializer(reservas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def reserva_area_detalle(request, idreserva):
    reserva = ReservaAreaService.obtener_reserva(idreserva)
    if reserva:
        serializer = ReservaAreaSerializer(reserva)
        return Response(serializer.data)
    return Response({'error': 'Reserva no encontrada'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def reserva_area_crear(request):
    serializer = ReservaAreaSerializer(data=request.data)
    if serializer.is_valid():
        ReservaAreaService.crear_reserva(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def reserva_area_actualizar(request, idreserva):
    serializer = ReservaAreaSerializer(data=request.data)
    if serializer.is_valid():
        ReservaAreaService.actualizar_reserva(idreserva, serializer.validated_data)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def reserva_area_eliminar(request, idreserva):
    ReservaAreaService.eliminar_reserva(idreserva)
    return Response({'mensaje': 'Reserva anulada'}, status=status.HTTP_204_NO_CONTENT)
