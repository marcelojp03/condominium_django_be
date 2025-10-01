from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from modules.ad.services.area_comun_service import AreaComunService
from modules.ad.dtos.area_comun_dto import AreaComunSerializer

@api_view(['GET'])
def area_comun_listar(request):
    areas = AreaComunService.listar_areas()
    serializer = AreaComunSerializer(areas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def area_comun_detalle(request, idarea):
    area = AreaComunService.obtener_area(idarea)
    if area:
        serializer = AreaComunSerializer(area)
        return Response(serializer.data)
    return Response({'error': 'Área común no encontrada'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def area_comun_crear(request):
    serializer = AreaComunSerializer(data=request.data)
    if serializer.is_valid():
        AreaComunService.crear_area(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def area_comun_actualizar(request, idarea):
    serializer = AreaComunSerializer(data=request.data)
    if serializer.is_valid():
        AreaComunService.actualizar_area(idarea, serializer.validated_data)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def area_comun_eliminar(request, idarea):
    AreaComunService.eliminar_area(idarea)
    return Response({'mensaje': 'Área común desactivada'}, status=status.HTTP_204_NO_CONTENT)
