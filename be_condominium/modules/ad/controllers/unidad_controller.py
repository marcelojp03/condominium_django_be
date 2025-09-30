from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from modules.ad.services.unidad_service import UnidadService
from modules.ad.dtos.unidad_dto import UnidadSerializer

@api_view(['GET'])
def unidad_listar(request):
    unidades = UnidadService.listar_unidades()
    serializer = UnidadSerializer(unidades, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def unidad_detalle(request, idunidad):
    unidad = UnidadService.obtener_unidad(idunidad)
    if unidad:
        serializer = UnidadSerializer(unidad)
        return Response(serializer.data)
    return Response({'error': 'Unidad no encontrada'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def unidad_crear(request):
    serializer = UnidadSerializer(data=request.data)
    if serializer.is_valid():
        UnidadService.crear_unidad(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def unidad_actualizar(request, idunidad):
    serializer = UnidadSerializer(data=request.data)
    if serializer.is_valid():
        UnidadService.actualizar_unidad(idunidad, serializer.validated_data)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def unidad_eliminar(request, idunidad):
    UnidadService.eliminar_unidad(idunidad)
    return Response({'mensaje': 'Unidad desactivada'}, status=status.HTTP_204_NO_CONTENT)
