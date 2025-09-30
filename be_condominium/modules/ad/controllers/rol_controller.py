from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models.rol import Rol
from ..dtos.rol_dto import RolSerializer,RolDetalleSerializer

@api_view(['GET', 'POST'])
def rol_listar_crear(request):
    if request.method == 'GET':
        roles = Rol.objects.all()
        serializer = RolSerializer(roles, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = RolSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def rol_detalle(request, pk):
    try:
        rol = Rol.objects.get(pk=pk)
    except Rol.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RolSerializer(rol)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = RolSerializer(rol, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        rol.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def rol_detalle_recursos(request, pk):
    try:
        rol = Rol.objects.get(pk=pk)
    except Rol.DoesNotExist:
        return Response({"error": "Rol no encontrado"}, status=404)

    serializer = RolDetalleSerializer(rol)
    return Response(serializer.data)