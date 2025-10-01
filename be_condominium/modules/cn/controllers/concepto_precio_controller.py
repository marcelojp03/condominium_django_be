from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from modules.cn.services.concepto_precio_service import ConceptoPrecioService
from modules.cn.dtos.concepto_precio_dto import ConceptoPrecioSerializer

@api_view(['GET'])
def concepto_precio_listar(request):
    conceptos = ConceptoPrecioService.listar_conceptos()
    serializer = ConceptoPrecioSerializer(conceptos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def concepto_precio_detalle(request, idconcepto):
    concepto = ConceptoPrecioService.obtener_concepto(idconcepto)
    if concepto:
        serializer = ConceptoPrecioSerializer(concepto)
        return Response(serializer.data)
    return Response({'error': 'Concepto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def concepto_precio_crear(request):
    serializer = ConceptoPrecioSerializer(data=request.data)
    if serializer.is_valid():
        ConceptoPrecioService.crear_concepto(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def concepto_precio_actualizar(request, idconcepto):
    serializer = ConceptoPrecioSerializer(data=request.data)
    if serializer.is_valid():
        ConceptoPrecioService.actualizar_concepto(idconcepto, serializer.validated_data)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def concepto_precio_eliminar(request, idconcepto):
    ConceptoPrecioService.eliminar_concepto(idconcepto)
    return Response({'mensaje': 'Concepto desactivado'}, status=status.HTTP_204_NO_CONTENT)
