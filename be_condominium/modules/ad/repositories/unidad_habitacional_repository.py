from ..models.unidad_habitacional import UnidadHabitacional

class UnidadHabitacionalRepository:
    def obtener_todos(self):
        return UnidadHabitacional.objects.all()
