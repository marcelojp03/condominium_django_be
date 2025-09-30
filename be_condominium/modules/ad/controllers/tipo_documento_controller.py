from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from modules.ad.services.tipo_documento_service import TipoDocumentoService
from modules.ad.dtos.tipo_documento_dto import TipoDocumentoSerializer

@api_view(['GET'])
def tipo_documento_listar(request):
    tipos = TipoDocumentoService.listar_tipos()
    serializer = TipoDocumentoSerializer(tipos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def tipo_documento_detalle(request, idtipo):
    tipo = TipoDocumentoService.obtener_tipo(idtipo)
    if tipo:
        serializer = TipoDocumentoSerializer(tipo)
        return Response(serializer.data)
    return Response({'error': 'Tipo no encontrado'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def tipo_documento_crear(request):
    serializer = TipoDocumentoSerializer(data=request.data)
    if serializer.is_valid():
        TipoDocumentoService.crear_tipo(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def tipo_documento_actualizar(request, idtipo):
    serializer = TipoDocumentoSerializer(data=request.data)
    if serializer.is_valid():
        TipoDocumentoService.actualizar_tipo(idtipo, serializer.validated_data)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def tipo_documento_eliminar(request, idtipo):
    TipoDocumentoService.eliminar_tipo(idtipo)
    return Response({'mensaje': 'Tipo de documento desactivado'}, status=status.HTTP_204_NO_CONTENT)
