from ..repositories.recurso_repository import RecursoRepository

class UnidadHabitacionalService:
    def __init__(self):
        self.repo = RecursoRepository()

    def listar_unidades_habitacionales(self):
        return self.repo.obtener_todos()
