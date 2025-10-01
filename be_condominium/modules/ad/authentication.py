from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import jwt
from modules.ad.models.usuario import Usuario

User = get_user_model()

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            usuario_id = payload.get('usuario_id')
            
            if not usuario_id:
                raise AuthenticationFailed('Token inválido.')
            
            try:
                usuario = Usuario.objects.get(id=usuario_id)
                # Crear un usuario de Django compatible para el sistema de permisos
                django_user, created = User.objects.get_or_create(
                    username=usuario.correo,
                    defaults={
                        'email': usuario.correo,
                        'is_active': True,
                        'is_staff': False,
                        'is_superuser': False
                    }
                )
                return (django_user, token)
                
            except Usuario.DoesNotExist:
                raise AuthenticationFailed('Usuario no encontrado.')
                
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expirado.')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Token inválido.')

    def authenticate_header(self, request):
        return 'Bearer'