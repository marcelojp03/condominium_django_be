from modules.ad.repositories.aviso_repository import AvisoRepository

class AvisoService:

    @staticmethod
    def listar_avisos():
        return AvisoRepository.listar()

    @staticmethod
    def obtener_aviso(idaviso):
        return AvisoRepository.obtener_por_id(idaviso)

    @staticmethod
    def crear_aviso(data):
        return AvisoRepository.crear(data)

    @staticmethod
    def actualizar_aviso(idaviso, data):
        return AvisoRepository.actualizar(idaviso, data)

    @staticmethod
    def eliminar_aviso(idaviso):
        return AvisoRepository.eliminar(idaviso)
