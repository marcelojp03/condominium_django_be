from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models.recurso import Recurso
from ..dtos.recurso_dto import RecursoSerializer

@api_view(['GET', 'POST'])
def recurso_listar_crear(request):
    if request.method == 'GET':
        recursos = Recurso.objects.all()
        serializer = RecursoSerializer(recursos, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = RecursoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
