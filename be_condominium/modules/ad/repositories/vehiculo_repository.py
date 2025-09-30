from modules.ad.models.vehiculo_model import Vehiculo

class VehiculoRepository:

    @staticmethod
    def listar():
        return Vehiculo.objects.filter(estado=True).order_by('placa')

    @staticmethod
    def obtener_por_id(idvehiculo):
        return Vehiculo.objects.filter(idvehiculo=idvehiculo).first()

    @staticmethod
    def crear(data):
        return Vehiculo.objects.create(**data)

    @staticmethod
    def actualizar(idvehiculo, data):
        Vehiculo.objects.filter(idvehiculo=idvehiculo).update(**data)

    @staticmethod
    def eliminar(idvehiculo):
        Vehiculo.objects.filter(idvehiculo=idvehiculo).update(estado=False)
