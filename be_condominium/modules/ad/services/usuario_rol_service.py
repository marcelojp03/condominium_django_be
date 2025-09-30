from ..repositories.usuario_rol_repository import UsuarioRolRepository

class UsuarioRolService:
    def __init__(self):
        self.repo = UsuarioRolRepository()

    def obtener_roles_de_usuario(self, usuario_id):
        return self.repo.obtener_por_usuario(usuario_id)

    def asignar_rol_a_usuario(self, usuario_id, rol_id):
        return self.repo.asignar_rol(usuario_id, rol_id)
