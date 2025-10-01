from ..models.subrecurso import Subrecurso

class SubrecursoRepository:
    def obtener_por_recurso(self, recurso_id):
        return Subrecurso.objects.filter(recurso_id=recurso_id)
