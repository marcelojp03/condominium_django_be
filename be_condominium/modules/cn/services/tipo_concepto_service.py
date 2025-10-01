from modules.cn.repositories.tipo_concepto_repository import TipoConceptoRepository

class TipoConceptoService:

    @staticmethod
    def listar_tipos():
        return TipoConceptoRepository.listar()

    @staticmethod
    def obtener_tipo(idtipo):
        return TipoConceptoRepository.obtener_por_id(idtipo)

    @staticmethod
    def crear_tipo(data):
        return TipoConceptoRepository.crear(data)

    @staticmethod
    def actualizar_tipo(idtipo, data):
        return TipoConceptoRepository.actualizar(idtipo, data)

    @staticmethod
    def eliminar_tipo(idtipo):
        return TipoConceptoRepository.eliminar(idtipo)
