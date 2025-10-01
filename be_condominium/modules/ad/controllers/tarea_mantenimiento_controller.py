from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from modules.ad.services.tarea_mantenimiento_service import TareaMantenimientoService
from modules.ad.dtos.tarea_mantenimiento_dto import TareaMantenimientoSerializer

@api_view(['GET'])
def tarea_mantenimiento_listar(request):
    tareas = TareaMantenimientoService.listar_tareas()
    serializer = TareaMantenimientoSerializer(tareas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def tarea_mantenimiento_detalle(request, idtarea):
    tarea = TareaMantenimientoService.obtener_tarea(idtarea)
    if tarea:
        serializer = TareaMantenimientoSerializer(tarea)
        return Response(serializer.data)
    return Response({'error': 'Tarea no encontrada'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def tarea_mantenimiento_crear(request):
    serializer = TareaMantenimientoSerializer(data=request.data)
    if serializer.is_valid():
        TareaMantenimientoService.crear_tarea(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def tarea_mantenimiento_actualizar(request, idtarea):
    serializer = TareaMantenimientoSerializer(data=request.data)
    if serializer.is_valid():
        TareaMantenimientoService.actualizar_tarea(idtarea, serializer.validated_data)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def tarea_mantenimiento_eliminar(request, idtarea):
    TareaMantenimientoService.eliminar_tarea(idtarea)
    return Response({'mensaje': 'Tarea anulada'}, status=status.HTTP_204_NO_CONTENT)
