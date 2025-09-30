from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models.rol_recurso import RolRecurso
from ..dtos.rol_recurso_dto import RolRecursoSerializer

@api_view(['GET', 'POST'])
def rol_recurso_listar_crear(request):
    if request.method == 'GET':
        permisos = RolRecurso.objects.all()
        serializer = RolRecursoSerializer(permisos, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = RolRecursoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
