from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from modules.ad.services.vehiculo_service import VehiculoService
from modules.ad.dtos.vehiculo_dto import VehiculoSerializer

@api_view(['GET'])
def vehiculo_listar(request):
    vehiculos = VehiculoService.listar_vehiculos()
    serializer = VehiculoSerializer(vehiculos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def vehiculo_detalle(request, idvehiculo):
    vehiculo = VehiculoService.obtener_vehiculo(idvehiculo)
    if vehiculo:
        serializer = VehiculoSerializer(vehiculo)
        return Response(serializer.data)
    return Response({'error': 'Vehículo no encontrado'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def vehiculo_crear(request):
    serializer = VehiculoSerializer(data=request.data)
    if serializer.is_valid():
        VehiculoService.crear_vehiculo(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def vehiculo_actualizar(request, idvehiculo):
    serializer = VehiculoSerializer(data=request.data)
    if serializer.is_valid():
        VehiculoService.actualizar_vehiculo(idvehiculo, serializer.validated_data)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def vehiculo_eliminar(request, idvehiculo):
    VehiculoService.eliminar_vehiculo(idvehiculo)
    return Response({'mensaje': 'Vehículo desactivado'}, status=status.HTTP_204_NO_CONTENT)
