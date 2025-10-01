from modules.ad.repositories.area_comun_repository import AreaComunRepository

class AreaComunService:

    @staticmethod
    def listar_areas():
        return AreaComunRepository.listar()

    @staticmethod
    def obtener_area(idarea):
        return AreaComunRepository.obtener_por_id(idarea)

    @staticmethod
    def crear_area(data):
        return AreaComunRepository.crear(data)

    @staticmethod
    def actualizar_area(idarea, data):
        return AreaComunRepository.actualizar(idarea, data)

    @staticmethod
    def eliminar_area(idarea):
        return AreaComunRepository.eliminar(idarea)
