from modules.ad.repositories.vehiculo_foto_repository import VehiculoFotoRepository

class VehiculoFotoService:

    @staticmethod
    def listar_fotos():
        return VehiculoFotoRepository.listar()

    @staticmethod
    def obtener_foto(idfoto):
        return VehiculoFotoRepository.obtener_por_id(idfoto)

    @staticmethod
    def crear_foto(data):
        return VehiculoFotoRepository.crear(data)

    @staticmethod
    def actualizar_foto(idfoto, data):
        return VehiculoFotoRepository.actualizar(idfoto, data)

    @staticmethod
    def eliminar_foto(idfoto):
        return VehiculoFotoRepository.eliminar(idfoto)
