from modules.ad.repositories.zona_repository import ZonaRepository

class ZonaService:

    @staticmethod
    def listar_zonas():
        return ZonaRepository.listar()

    @staticmethod
    def obtener_zona(idzona):
        return ZonaRepository.obtener_por_id(idzona)

    @staticmethod
    def crear_zona(data):
        return ZonaRepository.crear(data)

    @staticmethod
    def actualizar_zona(idzona, data):
        return ZonaRepository.actualizar(idzona, data)

    @staticmethod
    def eliminar_zona(idzona):
        return ZonaRepository.eliminar(idzona)
