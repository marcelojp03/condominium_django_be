from ..repositories.subrecurso_repository import SubrecursoRepository

class SubrecursoService:
    def __init__(self):
        self.repo = SubrecursoRepository()

    def obtener_subrecursos(self, recurso_id):
        return self.repo.obtener_por_recurso(recurso_id)
