from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from modules.cn.services.tipo_concepto_service import TipoConceptoService
from modules.cn.dtos.tipo_concepto_dto import TipoConceptoSerializer

@api_view(['GET'])
def tipo_concepto_listar(request):
    tipos = TipoConceptoService.listar_tipos()
    serializer = TipoConceptoSerializer(tipos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def tipo_concepto_detalle(request, idtipo):
    tipo = TipoConceptoService.obtener_tipo(idtipo)
    if tipo:
        serializer = TipoConceptoSerializer(tipo)
        return Response(serializer.data)
    return Response({'error': 'Tipo de concepto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def tipo_concepto_crear(request):
    serializer = TipoConceptoSerializer(data=request.data)
    if serializer.is_valid():
        TipoConceptoService.crear_tipo(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def tipo_concepto_actualizar(request, idtipo):
    serializer = TipoConceptoSerializer(data=request.data)
    if serializer.is_valid():
        TipoConceptoService.actualizar_tipo(idtipo, serializer.validated_data)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def tipo_concepto_eliminar(request, idtipo):
    TipoConceptoService.eliminar_tipo(idtipo)
    return Response({'mensaje': 'Tipo de concepto desactivado'}, status=status.HTTP_204_NO_CONTENT)
