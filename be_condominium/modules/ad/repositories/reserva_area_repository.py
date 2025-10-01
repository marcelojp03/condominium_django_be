from modules.ad.models.reserva_area_model import ReservaArea

class ReservaAreaRepository:

    @staticmethod
    def listar():
        return ReservaArea.objects.filter(estado=True).order_by('-fecha_reserva', 'hora_inicio')

    @staticmethod
    def obtener_por_id(idreserva):
        return ReservaArea.objects.filter(idreserva=idreserva).first()

    @staticmethod
    def crear(data):
        return ReservaArea.objects.create(**data)

    @staticmethod
    def actualizar(idreserva, data):
        ReservaArea.objects.filter(idreserva=idreserva).update(**data)

    @staticmethod
    def eliminar(idreserva):
        ReservaArea.objects.filter(idreserva=idreserva).update(estado=False)
