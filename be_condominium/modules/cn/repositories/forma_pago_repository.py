from modules.cn.models.forma_pago_model import FormaPago

class FormaPagoRepository:

    @staticmethod
    def listar():
        return FormaPago.objects.filter(estado=True).order_by('nombre')

    @staticmethod
    def obtener_por_id(idformapago):
        return FormaPago.objects.filter(idformapago=idformapago).first()

    @staticmethod
    def crear(data):
        return FormaPago.objects.create(**data)

    @staticmethod
    def actualizar(idformapago, data):
        FormaPago.objects.filter(idformapago=idformapago).update(**data)

    @staticmethod
    def eliminar(idformapago):
        FormaPago.objects.filter(idformapago=idformapago).update(estado=False)
