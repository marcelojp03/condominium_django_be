from modules.ad.repositories.vehiculo_repository import VehiculoRepository

class VehiculoService:

    @staticmethod
    def listar_vehiculos():
        return VehiculoRepository.listar()

    @staticmethod
    def obtener_vehiculo(idvehiculo):
        return VehiculoRepository.obtener_por_id(idvehiculo)

    @staticmethod
    def crear_vehiculo(data):
        return VehiculoRepository.crear(data)

    @staticmethod
    def actualizar_vehiculo(idvehiculo, data):
        return VehiculoRepository.actualizar(idvehiculo, data)

    @staticmethod
    def eliminar_vehiculo(idvehiculo):
        return VehiculoRepository.eliminar(idvehiculo)
