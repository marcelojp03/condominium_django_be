from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models.usuario_rol import UsuarioRol
from ..dtos.usuario_rol_dto import UsuarioRolSerializer

@api_view(['GET', 'POST'])
def usuario_rol_listar_crear(request):
    if request.method == 'GET':
        asignaciones = UsuarioRol.objects.all()
        serializer = UsuarioRolSerializer(asignaciones, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UsuarioRolSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
