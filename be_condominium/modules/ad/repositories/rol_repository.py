from ..models.rol import Rol

class RolRepository:
    def obtener_todos(self):
        return Rol.objects.all()

    def buscar_por_id(self, id):
        return Rol.objects.filter(id=id).first()
