from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from modules.ad.services.zona_service import ZonaService
from modules.ad.dtos.zona_dto import ZonaSerializer

@api_view(['GET'])
def zona_listar(request):
    zonas = ZonaService.listar_zonas()
    serializer = ZonaSerializer(zonas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def zona_detalle(request, idzona):
    zona = ZonaService.obtener_zona(idzona)
    if zona:
        serializer = ZonaSerializer(zona)
        return Response(serializer.data)
    return Response({'error': 'Zona no encontrada'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def zona_crear(request):
    serializer = ZonaSerializer(data=request.data)
    if serializer.is_valid():
        ZonaService.crear_zona(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def zona_actualizar(request, idzona):
    serializer = ZonaSerializer(data=request.data)
    if serializer.is_valid():
        ZonaService.actualizar_zona(idzona, serializer.validated_data)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def zona_eliminar(request, idzona):
    ZonaService.eliminar_zona(idzona)
    return Response({'mensaje': 'Zona desactivada'}, status=status.HTTP_204_NO_CONTENT)
