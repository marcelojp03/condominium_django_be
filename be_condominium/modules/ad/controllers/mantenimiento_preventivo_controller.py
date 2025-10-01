from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from modules.ad.services.mantenimiento_preventivo_service import MantenimientoPreventivoService
from modules.ad.dtos.mantenimiento_preventivo_dto import MantenimientoPreventivoSerializer

@api_view(['GET'])
def mantenimiento_preventivo_listar(request):
    registros = MantenimientoPreventivoService.listar_preventivos()
    serializer = MantenimientoPreventivoSerializer(registros, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def mantenimiento_preventivo_detalle(request, idpreventivo):
    registro = MantenimientoPreventivoService.obtener_preventivo(idpreventivo)
    if registro:
        serializer = MantenimientoPreventivoSerializer(registro)
        return Response(serializer.data)
    return Response({'error': 'Registro no encontrado'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def mantenimiento_preventivo_crear(request):
    serializer = MantenimientoPreventivoSerializer(data=request.data)
    if serializer.is_valid():
        MantenimientoPreventivoService.crear_preventivo(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def mantenimiento_preventivo_actualizar(request, idpreventivo):
    serializer = MantenimientoPreventivoSerializer(data=request.data)
    if serializer.is_valid():
        MantenimientoPreventivoService.actualizar_preventivo(idpreventivo, serializer.validated_data)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def mantenimiento_preventivo_eliminar(request, idpreventivo):
    MantenimientoPreventivoService.eliminar_preventivo(idpreventivo)
    return Response({'mensaje': 'Registro desactivado'}, status=status.HTTP_204_NO_CONTENT)
