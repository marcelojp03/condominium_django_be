from modules.ad.models.mantenimiento_preventivo_model import MantenimientoPreventivo

class MantenimientoPreventivoRepository:

    @staticmethod
    def listar():
        return MantenimientoPreventivo.objects.filter(estado=True).order_by('frecuencia', 'area__nombre')

    @staticmethod
    def obtener_por_id(idpreventivo):
        return MantenimientoPreventivo.objects.filter(idpreventivo=idpreventivo).first()

    @staticmethod
    def crear(data):
        return MantenimientoPreventivo.objects.create(**data)

    @staticmethod
    def actualizar(idpreventivo, data):
        MantenimientoPreventivo.objects.filter(idpreventivo=idpreventivo).update(**data)

    @staticmethod
    def eliminar(idpreventivo):
        MantenimientoPreventivo.objects.filter(idpreventivo=idpreventivo).update(estado=False)
