from modules.cn.repositories.cuota_repository import CuotaRepository
from django.utils import timezone

class CuotaService:

    @staticmethod
    def listar_cuotas(residente_id=None, estado=None, fecha_desde=None, fecha_hasta=None):
        """
        🔴 MÉTODO ACTUALIZADO - Soporta filtros para app móvil
        """
        return CuotaRepository.listar(
            residente_id=residente_id,
            estado=estado,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta
        )

    @staticmethod
    def obtener_cuota(idcuota):
        return CuotaRepository.obtener_por_id(idcuota)

    @staticmethod
    def crear_cuota(data):
        return CuotaRepository.crear(data)

    @staticmethod
    def actualizar_cuota(idcuota, data):
        return CuotaRepository.actualizar(idcuota, data)

    @staticmethod
    def eliminar_cuota(idcuota):
        return CuotaRepository.eliminar(idcuota)
    
    @staticmethod
    def pagar_cuota(idcuota, forma_pago_id, monto, comprobante=''):
        """
        🔴 MÉTODO NUEVO - CRÍTICO PARA APP MÓVIL
        Registra el pago de una cuota
        """
        cuota = CuotaRepository.obtener_por_id(idcuota)
        if not cuota:
            return None
        
        data = {
            'estado_pago': 'PAGADO',
            'fecha_pago': timezone.now(),
            'forma_pago_id': forma_pago_id,
            'monto': monto,
            'observaciones': f'Pago registrado desde app móvil. {comprobante}'
        }
        
        CuotaRepository.actualizar(idcuota, data)
        return CuotaRepository.obtener_por_id(idcuota)
