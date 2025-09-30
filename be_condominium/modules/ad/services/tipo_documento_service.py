from modules.ad.repositories.tipo_documento_repository import TipoDocumentoRepository

class TipoDocumentoService:

    @staticmethod
    def listar_tipos():
        return TipoDocumentoRepository.listar()

    @staticmethod
    def obtener_tipo(idtipo):
        return TipoDocumentoRepository.obtener_por_id(idtipo)

    @staticmethod
    def crear_tipo(data):
        return TipoDocumentoRepository.crear(data)

    @staticmethod
    def actualizar_tipo(idtipo, data):
        return TipoDocumentoRepository.actualizar(idtipo, data)

    @staticmethod
    def eliminar_tipo(idtipo):
        return TipoDocumentoRepository.eliminar(idtipo)
