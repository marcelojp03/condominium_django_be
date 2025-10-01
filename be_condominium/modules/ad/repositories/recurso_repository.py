from ..models.recurso import Recurso

class RecursoRepository:
    def obtener_todos(self):
        return Recurso.objects.all()
