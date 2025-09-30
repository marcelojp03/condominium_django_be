from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from modules.ad.services.vehiculo_foto_service import VehiculoFotoService
from modules.ad.dtos.vehiculo_foto_dto import VehiculoFotoSerializer

@api_view(['GET'])
def vehiculo_foto_listar(request):
    fotos = VehiculoFotoService.listar_fotos()
    serializer = VehiculoFotoSerializer(fotos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def vehiculo_foto_detalle(request, idfoto):
    foto = VehiculoFotoService.obtener_foto(idfoto)
    if foto:
        serializer = VehiculoFotoSerializer(foto)
        return Response(serializer.data)
    return Response({'error': 'Foto no encontrada'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def vehiculo_foto_crear(request):
    serializer = VehiculoFotoSerializer(data=request.data)
    if serializer.is_valid():
        VehiculoFotoService.crear_foto(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def vehiculo_foto_actualizar(request, idfoto):
    serializer = VehiculoFotoSerializer(data=request.data)
    if serializer.is_valid():
        VehiculoFotoService.actualizar_foto(idfoto, serializer.validated_data)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def vehiculo_foto_eliminar(request, idfoto):
    VehiculoFotoService.eliminar_foto(idfoto)
    return Response({'mensaje': 'Foto desactivada'}, status=status.HTTP_204_NO_CONTENT)
