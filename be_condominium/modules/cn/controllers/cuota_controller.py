from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from modules.cn.services.cuota_service import CuotaService
from modules.cn.dtos.cuota_dto import CuotaSerializer

@api_view(['GET'])
def cuota_listar(request):
    cuotas = CuotaService.listar_cuotas()
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
