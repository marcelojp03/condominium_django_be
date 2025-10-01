from modules.ad.repositories.residente_foto_repository import ResidenteFotoRepository

class ResidenteFotoService:

    @staticmethod
    def listar_fotos():
        return ResidenteFotoRepository.listar()

    @staticmethod
    def obtener_foto(idfoto):
        return ResidenteFotoRepository.obtener_por_id(idfoto)

    @staticmethod
    def crear_foto(data):
        return ResidenteFotoRepository.crear(data)

    @staticmethod
    def actualizar_foto(idfoto, data):
        return ResidenteFotoRepository.actualizar(idfoto, data)

    @staticmethod
    def eliminar_foto(idfoto):
        return ResidenteFotoRepository.eliminar(idfoto)
