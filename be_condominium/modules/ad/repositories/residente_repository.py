from modules.ad.models.residente_model import Residente

class ResidenteRepository:

    @staticmethod
    def listar():
        return Residente.objects.filter(estado=True).order_by('apellido1', 'nombres')

    @staticmethod
    def obtener_por_id(idresidente):
        return Residente.objects.filter(idresidente=idresidente).first()

    @staticmethod
    def crear(data):
        return Residente.objects.create(**data)

    @staticmethod
    def actualizar(idresidente, data):
        Residente.objects.filter(idresidente=idresidente).update(**data)

    @staticmethod
    def eliminar(idresidente):
        Residente.objects.filter(idresidente=idresidente).update(estado=False)
