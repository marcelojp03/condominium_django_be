from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from modules.cn.services.unidad_concepto_service import UnidadConceptoService
from modules.cn.dtos.unidad_concepto_dto import UnidadConceptoSerializer

@api_view(['GET'])
def unidad_concepto_listar(request):
    asignaciones = UnidadConceptoService.listar_asignaciones()
    serializer = UnidadConceptoSerializer(asignaciones, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def unidad_concepto_detalle(request, id):
    asignacion = UnidadConceptoService.obtener_asignacion(id)
    if asignacion:
        serializer = UnidadConceptoSerializer(asignacion)
        return Response(serializer.data)
    return Response({'error': 'Asignación no encontrada'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def unidad_concepto_crear(request):
    serializer = UnidadConceptoSerializer(data=request.data)
    if serializer.is_valid():
        UnidadConceptoService.crear_asignacion(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def unidad_concepto_actualizar(request, id):
    serializer = UnidadConceptoSerializer(data=request.data)
    if serializer.is_valid():
        UnidadConceptoService.actualizar_asignacion(id, serializer.validated_data)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def unidad_concepto_eliminar(request, id):
    UnidadConceptoService.eliminar_asignacion(id)
    return Response({'mensaje': 'Asignación desactivada'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def unidad_concepto_por_unidad(request, idunidad):
    asignaciones = UnidadConceptoService.listar_por_unidad(idunidad)

    vigentes = [a for a in asignaciones if a.estado is True]
    pagadas = [a for a in asignaciones if a.estado is False]

    serializer_vigentes = UnidadConceptoSerializer(vigentes, many=True)
    serializer_pagadas = UnidadConceptoSerializer(pagadas, many=True)

    return Response({
        "codigo_unidad": vigentes[0].unidad.codigo if vigentes else pagadas[0].unidad.codigo if pagadas else None,
        "vigentes": serializer_vigentes.data,
        "pagadas": serializer_pagadas.data
    })

