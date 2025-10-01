from modules.cn.repositories.unidad_concepto_repository import UnidadConceptoRepository

class UnidadConceptoService:

    @staticmethod
    def listar_asignaciones():
        return UnidadConceptoRepository.listar()

    @staticmethod
    def obtener_asignacion(id):
        return UnidadConceptoRepository.obtener_por_id(id)

    @staticmethod
    def crear_asignacion(data):
        return UnidadConceptoRepository.crear(data)

    @staticmethod
    def actualizar_asignacion(id, data):
        return UnidadConceptoRepository.actualizar(id, data)

    @staticmethod
    def eliminar_asignacion(id):
        return UnidadConceptoRepository.eliminar(id)
