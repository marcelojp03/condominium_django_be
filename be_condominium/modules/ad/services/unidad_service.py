from modules.ad.repositories.unidad_repository import UnidadRepository

class UnidadService:

    @staticmethod
    def listar_unidades():
        return UnidadRepository.listar()

    @staticmethod
    def obtener_unidad(idunidad):
        return UnidadRepository.obtener_por_id(idunidad)

    @staticmethod
    def crear_unidad(data):
        return UnidadRepository.crear(data)

    @staticmethod
    def actualizar_unidad(idunidad, data):
        return UnidadRepository.actualizar(idunidad, data)

    @staticmethod
    def eliminar_unidad(idunidad):
        return UnidadRepository.eliminar(idunidad)
