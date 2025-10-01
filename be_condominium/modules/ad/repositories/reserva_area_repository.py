from modules.ad.models.reserva_area_model import ReservaArea

class ReservaAreaRepository:

    @staticmethod
    def listar(residente_id=None, estado=None):
        """
        🔴 MÉTODO ACTUALIZADO - Soporta filtros para app móvil
        """
        queryset = ReservaArea.objects.select_related('area', 'residente')
        
        # Filtro por residente (crítico para app móvil)
        if residente_id:
            queryset = queryset.filter(residente_id=residente_id)
        
        # Filtro por estado de reserva
        if estado:
            queryset = queryset.filter(estado_reserva=estado)
        else:
            queryset = queryset.filter(estado=True)  # Solo activas por defecto
        
        return queryset.order_by('-fecha_reserva', 'hora_inicio')

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
