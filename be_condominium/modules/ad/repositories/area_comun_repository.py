from modules.ad.models.area_comun_model import AreaComun

class AreaComunRepository:

    @staticmethod
    def listar():
        return AreaComun.objects.filter(estado=True).order_by('nombre')

    @staticmethod
    def obtener_por_id(idarea):
        return AreaComun.objects.filter(idarea=idarea).first()

    @staticmethod
    def crear(data):
        return AreaComun.objects.create(**data)

    @staticmethod
    def actualizar(idarea, data):
        AreaComun.objects.filter(idarea=idarea).update(**data)

    @staticmethod
    def eliminar(idarea):
        AreaComun.objects.filter(idarea=idarea).update(estado=False)
