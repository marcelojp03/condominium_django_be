from modules.ad.repositories.reserva_area_repository import ReservaAreaRepository

class ReservaAreaService:

    @staticmethod
    def listar_reservas(residente_id=None, estado=None):
        """
        🔴 MÉTODO ACTUALIZADO - Soporta filtros para app móvil
        """
        return ReservaAreaRepository.listar(residente_id=residente_id, estado=estado)

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
