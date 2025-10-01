from modules.ad.repositories.reserva_area_repository import ReservaAreaRepository

class ReservaAreaService:

    @staticmethod
    def listar_reservas():
        return ReservaAreaRepository.listar()

    @staticmethod
    def obtener_reserva(idreserva):
        return ReservaAreaRepository.obtener_por_id(idreserva)

    @staticmethod
    def crear_reserva(data):
        return ReservaAreaRepository.crear(data)

    @staticmethod
    def actualizar_reserva(idreserva, data):
        return ReservaAreaRepository.actualizar(idreserva, data)

    @staticmethod
    def eliminar_reserva(idreserva):
        return ReservaAreaRepository.eliminar(idreserva)
