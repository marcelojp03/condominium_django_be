from modules.ad.models.vehiculo_foto_model import VehiculoFoto

class VehiculoFotoRepository:

    @staticmethod
    def listar():
        return VehiculoFoto.objects.filter(estado=True).order_by('-fecha_registro')

    @staticmethod
    def obtener_por_id(idfoto):
        return VehiculoFoto.objects.filter(idfoto=idfoto).first()

    @staticmethod
    def crear(data):
        return VehiculoFoto.objects.create(**data)

    @staticmethod
    def actualizar(idfoto, data):
        VehiculoFoto.objects.filter(idfoto=idfoto).update(**data)

    @staticmethod
    def eliminar(idfoto):
        VehiculoFoto.objects.filter(idfoto=idfoto).update(estado=False)
