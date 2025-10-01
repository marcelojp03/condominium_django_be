from modules.ad.repositories.residente_repository import ResidenteRepository

class ResidenteService:

    @staticmethod
    def listar_residentes():
        return ResidenteRepository.listar()

    @staticmethod
    def obtener_residente(idresidente):
        return ResidenteRepository.obtener_por_id(idresidente)

    @staticmethod
    def crear_residente(data):
        return ResidenteRepository.crear(data)

    @staticmethod
    def actualizar_residente(idresidente, data):
        return ResidenteRepository.actualizar(idresidente, data)

    @staticmethod
    def eliminar_residente(idresidente):
        return ResidenteRepository.eliminar(idresidente)
