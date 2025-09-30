from ..repositories.rol_recurso_repository import RolRecursoRepository

class RolRecursoService:
    def __init__(self):
        self.repo = RolRecursoRepository()

    def obtener_permisos_por_rol(self, rol_id):
        return self.repo.obtener_por_rol(rol_id)

    def asignar_permiso(self, rol_id, recurso_id, subrecurso_id):
        return self.repo.asignar_permiso(rol_id, recurso_id, subrecurso_id)
