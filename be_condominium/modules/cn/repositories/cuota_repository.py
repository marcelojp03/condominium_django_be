from modules.cn.models.cuota_model import Cuota
from modules.ad.models.unidad_model import Unidad
from modules.ad.models.residente_model import Residente

class CuotaRepository:

    @staticmethod
    def listar(residente_id=None, estado=None, fecha_desde=None, fecha_hasta=None):
        """
        🔴 MÉTODO ACTUALIZADO - Soporta filtros para app móvil
        """
        queryset = Cuota.objects.select_related('unidad', 'concepto', 'forma_pago')
        
        # Filtro por residente (crítico para app móvil)
        if residente_id:
            # Obtener unidades del residente
            unidades_ids = Unidad.objects.filter(
                residente__idresidente=residente_id
            ).values_list('idunidad', flat=True)
            queryset = queryset.filter(unidad_id__in=unidades_ids)
        
        # Filtro por estado
        if estado:
            queryset = queryset.filter(estado_pago=estado)
        
        # Filtro por rango de fechas
        if fecha_desde:
            queryset = queryset.filter(periodo__gte=fecha_desde)
        if fecha_hasta:
            queryset = queryset.filter(periodo__lte=fecha_hasta)
        
        return queryset.order_by('-periodo', 'unidad__codigo')

    @staticmethod
    def obtener_por_id(idcuota):
        return Cuota.objects.filter(idcuota=idcuota).first()

    @staticmethod
    def crear(data):
        return Cuota.objects.create(**data)

    @staticmethod
    def actualizar(idcuota, data):
        Cuota.objects.filter(idcuota=idcuota).update(**data)

    @staticmethod
    def eliminar(idcuota):
        Cuota.objects.filter(idcuota=idcuota).update(estado_pago='ANULADO')
