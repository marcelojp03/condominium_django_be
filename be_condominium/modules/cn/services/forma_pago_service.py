from modules.cn.repositories.forma_pago_repository import FormaPagoRepository

class FormaPagoService:

    @staticmethod
    def listar_formas():
        return FormaPagoRepository.listar()

    @staticmethod
    def obtener_forma(idformapago):
        return FormaPagoRepository.obtener_por_id(idformapago)

    @staticmethod
    def crear_forma(data):
        return FormaPagoRepository.crear(data)

    @staticmethod
    def actualizar_forma(idformapago, data):
        return FormaPagoRepository.actualizar(idformapago, data)

    @staticmethod
    def eliminar_forma(idformapago):
        return FormaPagoRepository.eliminar(idformapago)
