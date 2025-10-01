from modules.ad.models.tarea_mantenimiento_model import TareaMantenimiento

class TareaMantenimientoRepository:

    @staticmethod
    def listar():
        return TareaMantenimiento.objects.order_by('-fecha_programada')

    @staticmethod
    def obtener_por_id(idtarea):
        return TareaMantenimiento.objects.filter(idtarea=idtarea).first()

    @staticmethod
    def crear(data):
        return TareaMantenimiento.objects.create(**data)

    @staticmethod
    def actualizar(idtarea, data):
        TareaMantenimiento.objects.filter(idtarea=idtarea).update(**data)

    @staticmethod
    def eliminar(idtarea):
        TareaMantenimiento.objects.filter(idtarea=idtarea).update(estado='ANULADA')
