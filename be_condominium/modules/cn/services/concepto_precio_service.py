from modules.cn.repositories.concepto_precio_repository import ConceptoPrecioRepository

class ConceptoPrecioService:

    @staticmethod
    def listar_conceptos():
        return ConceptoPrecioRepository.listar()

    @staticmethod
    def obtener_concepto(idconcepto):
        return ConceptoPrecioRepository.obtener_por_id(idconcepto)

    @staticmethod
    def crear_concepto(data):
        return ConceptoPrecioRepository.crear(data)

    @staticmethod
    def actualizar_concepto(idconcepto, data):
        return ConceptoPrecioRepository.actualizar(idconcepto, data)

    @staticmethod
    def eliminar_concepto(idconcepto):
        return ConceptoPrecioRepository.eliminar(idconcepto)
