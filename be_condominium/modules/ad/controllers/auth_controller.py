from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from ..models.usuario import Usuario
import jwt
from django.conf import settings

@api_view(['POST'])
def login(request):
    correo = request.data.get('correo')
    password = request.data.get('password')

    try:
        usuario = Usuario.objects.get(correo=correo)
        if check_password(password, usuario.password):
            payload = {
                'usuario_id': usuario.id,
                'correo': usuario.correo,
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            return Response({'codigo': 0,'mensaje':"OK",'token': token, 'usuario_id': usuario.id}, status=status.HTTP_200_OK)
        else:
            return Response({'codigo': 1,'mensaje': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
    except Usuario.DoesNotExist:
        return Response({'message': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
