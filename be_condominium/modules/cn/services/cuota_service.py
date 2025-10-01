from modules.cn.repositories.cuota_repository import CuotaRepository

class CuotaService:

    @staticmethod
    def listar_cuotas():
        return CuotaRepository.listar()

    @staticmethod
    def obtener_cuota(idcuota):
        return CuotaRepository.obtener_por_id(idcuota)

    @staticmethod
    def crear_cuota(data):
        return CuotaRepository.crear(data)

    @staticmethod
    def actualizar_cuota(idcuota, data):
        return CuotaRepository.actualizar(idcuota, data)

    @staticmethod
    def eliminar_cuota(idcuota):
        return CuotaRepository.eliminar(idcuota)
