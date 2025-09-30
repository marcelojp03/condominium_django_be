from ..models.usuario_rol import UsuarioRol

class UsuarioRolRepository:
    def obtener_por_usuario(self, usuario_id):
        return UsuarioRol.objects.filter(usuario_id=usuario_id)

    def asignar_rol(self, usuario_id, rol_id):
        return UsuarioRol.objects.create(usuario_id=usuario_id, rol_id=rol_id)
