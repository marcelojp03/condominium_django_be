from modules.ad.models.zona_model import Zona

class ZonaRepository:

    @staticmethod
    def listar():
        return Zona.objects.filter(estado=True).order_by('nombre')

    @staticmethod
    def obtener_por_id(idzona):
        return Zona.objects.filter(idzona=idzona).first()

    @staticmethod
    def crear(data):
        return Zona.objects.create(**data)

    @staticmethod
    def actualizar(idzona, data):
        Zona.objects.filter(idzona=idzona).update(**data)

    @staticmethod
    def eliminar(idzona):
        Zona.objects.filter(idzona=idzona).update(estado=False)
