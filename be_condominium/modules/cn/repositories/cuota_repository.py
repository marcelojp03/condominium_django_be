from modules.cn.models.cuota_model import Cuota

class CuotaRepository:

    @staticmethod
    def listar():
        return Cuota.objects.order_by('-periodo', 'unidad__codigo')

    @staticmethod
    def obtener_por_id(idcuota):
        return Cuota.objects.filter(idcuota=idcuota).first()

    @staticmethod
    def crear(data):
        return Cuota.objects.create(**data)

    @staticmethod
    def actualizar(idcuota, data):
        Cuota.objects.filter(idcuota=idcuota).update(**data)

    @staticmethod
    def eliminar(idcuota):
        Cuota.objects.filter(idcuota=idcuota).update(estado_pago='ANULADO')
