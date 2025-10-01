from modules.ad.models.usuario import Usuario
from modules.ad.models.usuario_rol import UsuarioRol
from modules.ad.models.rol import Rol
from django.contrib.auth.hashers import make_password

def listar_todos():
    return Usuario.objects.all()

def obtener_por_id(usuario_id):
    return Usuario.objects.filter(id=usuario_id).first()

def crear(datos, rol_id=None):
    password = datos.pop('password', None)
    rol_id = datos.pop('rol_id', rol_id)  # extrae rol_id si viene en el serializer
    usuario = Usuario(**datos)
    if password:
        usuario.password = make_password(password)
    usuario.save()

    if rol_id:
        try:
            rol = Rol.objects.get(id=rol_id)
            UsuarioRol.objects.create(usuario=usuario, rol=rol)
        except Rol.DoesNotExist:
            # Puedes loguear el error o lanzar una excepción si lo prefieres
            pass

    return usuario


def actualizar(usuario, datos, rol_id=None):
    password = datos.pop('password', None)
    for key, value in datos.items():
        setattr(usuario, key, value)
    if password:
        usuario.password = make_password(password)
    usuario.save()

    if rol_id:
        try:
            rol = Rol.objects.get(id=rol_id)
            # Elimina roles anteriores si solo debe tener uno
            UsuarioRol.objects.filter(usuario=usuario).delete()
            UsuarioRol.objects.create(usuario=usuario, rol=rol)
        except Rol.DoesNotExist:
            pass

    return usuario

