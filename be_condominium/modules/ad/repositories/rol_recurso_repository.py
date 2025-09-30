from ..models.rol_recurso import RolRecurso

class RolRecursoRepository:
    def obtener_por_rol(self, rol_id):
        return RolRecurso.objects.filter(rol_id=rol_id)

    def asignar_permiso(self, rol_id, recurso_id, subrecurso_id):
        return RolRecurso.objects.create(
            rol_id=rol_id,
            recurso_id=recurso_id,
            subrecurso_id=subrecurso_id
        )
