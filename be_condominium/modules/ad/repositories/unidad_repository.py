from modules.ad.models.unidad_model import Unidad

class UnidadRepository:

    @staticmethod
    def listar():
        return Unidad.objects.filter(estado=True).order_by('codigo')

    @staticmethod
    def obtener_por_id(idunidad):
        return Unidad.objects.filter(idunidad=idunidad).first()

    @staticmethod
    def crear(data):
        return Unidad.objects.create(**data)

    @staticmethod
    def actualizar(idunidad, data):
        Unidad.objects.filter(idunidad=idunidad).update(**data)

    @staticmethod
    def eliminar(idunidad):
        Unidad.objects.filter(idunidad=idunidad).update(estado=False)
