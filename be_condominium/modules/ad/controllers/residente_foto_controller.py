from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from modules.ad.services.residente_foto_service import ResidenteFotoService
from modules.ad.dtos.residente_foto_dto import ResidenteFotoSerializer

@api_view(['GET'])
def residente_foto_listar(request):
    fotos = ResidenteFotoService.listar_fotos()
    serializer = ResidenteFotoSerializer(fotos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def residente_foto_detalle(request, idfoto):
    foto = ResidenteFotoService.obtener_foto(idfoto)
    if foto:
        serializer = ResidenteFotoSerializer(foto)
        return Response(serializer.data)
    return Response({'error': 'Foto no encontrada'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def residente_foto_crear(request):
    serializer = ResidenteFotoSerializer(data=request.data)
    if serializer.is_valid():
        ResidenteFotoService.crear_foto(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def residente_foto_actualizar(request, idfoto):
    serializer = ResidenteFotoSerializer(data=request.data)
    if serializer.is_valid():
        ResidenteFotoService.actualizar_foto(idfoto, serializer.validated_data)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def residente_foto_eliminar(request, idfoto):
    ResidenteFotoService.eliminar_foto(idfoto)
    return Response({'mensaje': 'Foto desactivada'}, status=status.HTTP_204_NO_CONTENT)
