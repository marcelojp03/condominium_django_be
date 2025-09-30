from ..repositories.rol_repository import RolRepository

class RolService:
    def __init__(self):
        self.repo = RolRepository()

    def listar_roles(self):
        return self.repo.obtener_todos()
