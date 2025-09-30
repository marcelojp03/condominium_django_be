from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from modules.ad.services.aviso_service import AvisoService
from modules.ad.dtos.aviso_dto import AvisoSerializer

@api_view(['GET'])
def aviso_listar(request):
    avisos = AvisoService.listar_avisos()
    serializer = AvisoSerializer(avisos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def aviso_detalle(request, idaviso):
    aviso = AvisoService.obtener_aviso(idaviso)
    if aviso:
        serializer = AvisoSerializer(aviso)
        return Response(serializer.data)
    return Response({'error': 'Aviso no encontrado'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def aviso_crear(request):
    serializer = AvisoSerializer(data=request.data)
    if serializer.is_valid():
        AvisoService.crear_aviso(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def aviso_actualizar(request, idaviso):
    serializer = AvisoSerializer(data=request.data)
    if serializer.is_valid():
        AvisoService.actualizar_aviso(idaviso, serializer.validated_data)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def aviso_eliminar(request, idaviso):
    AvisoService.eliminar_aviso(idaviso)
    return Response({'mensaje': 'Aviso desactivado'}, status=status.HTTP_204_NO_CONTENT)
