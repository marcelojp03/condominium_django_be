from modules.ad.models.aviso_model import Aviso

class AvisoRepository:

    @staticmethod
    def listar():
        return Aviso.objects.filter(estado=True).order_by('-fecha_publicacion')

    @staticmethod
    def obtener_por_id(idaviso):
        return Aviso.objects.filter(idaviso=idaviso).first()

    @staticmethod
    def crear(data):
        return Aviso.objects.create(**data)

    @staticmethod
    def actualizar(idaviso, data):
        Aviso.objects.filter(idaviso=idaviso).update(**data)

    @staticmethod
    def eliminar(idaviso):
        Aviso.objects.filter(idaviso=idaviso).update(estado=False)
