from modules.ad.repositories.mantenimiento_preventivo_repository import MantenimientoPreventivoRepository

class MantenimientoPreventivoService:

    @staticmethod
    def listar_preventivos():
        return MantenimientoPreventivoRepository.listar()

    @staticmethod
    def obtener_preventivo(idpreventivo):
        return MantenimientoPreventivoRepository.obtener_por_id(idpreventivo)

    @staticmethod
    def crear_preventivo(data):
        return MantenimientoPreventivoRepository.crear(data)

    @staticmethod
    def actualizar_preventivo(idpreventivo, data):
        return MantenimientoPreventivoRepository.actualizar(idpreventivo, data)

    @staticmethod
    def eliminar_preventivo(idpreventivo):
        return MantenimientoPreventivoRepository.eliminar(idpreventivo)
