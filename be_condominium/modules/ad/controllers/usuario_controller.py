from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from modules.ad.services import usuario_service
from modules.ad.dtos.usuario_dto import UsuarioSerializer

@api_view(['GET'])
def listar_usuarios(request):
    usuarios = usuario_service.obtener_todos()
    serializer = UsuarioSerializer(usuarios, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def obtener_usuario(request, usuario_id):
    usuario = usuario_service.obtener(usuario_id)
    if usuario:
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data)
    return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def crear_usuario(request):
    rol_id = request.data.get('rol_id')
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        usuario = usuario_service.crear(serializer.validated_data, rol_id)
        return Response(UsuarioSerializer(usuario).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def actualizar_usuario(request, usuario_id):
    usuario = usuario_service.obtener(usuario_id)
    if not usuario:
        return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UsuarioSerializer(usuario, data=request.data)
    if serializer.is_valid():
        usuario = usuario_service.actualizar(usuario_id, serializer.validated_data)
        return Response(UsuarioSerializer(usuario).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def eliminar_usuario(request, usuario_id):
    eliminado = usuario_service.eliminar(usuario_id)
    if eliminado:
        return Response({"mensaje": "Usuario eliminado"}, status=status.HTTP_204_NO_CONTENT)
    return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
