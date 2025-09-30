from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from modules.ad.services.residente_service import ResidenteService
from modules.ad.dtos.residente_dto import ResidenteSerializer

@api_view(['GET'])
def residente_listar(request):
    residentes = ResidenteService.listar_residentes()
    serializer = ResidenteSerializer(residentes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def residente_detalle(request, idresidente):
    residente = ResidenteService.obtener_residente(idresidente)
    if residente:
        serializer = ResidenteSerializer(residente)
        return Response(serializer.data)
    return Response({'error': 'Residente no encontrado'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def residente_crear(request):
    serializer = ResidenteSerializer(data=request.data)
    if serializer.is_valid():
        ResidenteService.crear_residente(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def residente_actualizar(request, idresidente):
    serializer = ResidenteSerializer(data=request.data)
    if serializer.is_valid():
        ResidenteService.actualizar_residente(idresidente, serializer.validated_data)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def residente_eliminar(request, idresidente):
    ResidenteService.eliminar_residente(idresidente)
    return Response({'mensaje': 'Residente desactivado'}, status=status.HTTP_204_NO_CONTENT)
