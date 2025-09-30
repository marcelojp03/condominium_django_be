from ..repositories.recurso_repository import RecursoRepository

class RecursoService:
    def __init__(self):
        self.repo = RecursoRepository()

    def listar_recursos(self):
        return self.repo.obtener_todos()
