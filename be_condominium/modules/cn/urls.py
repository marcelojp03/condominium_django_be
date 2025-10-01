from django.urls import path
from modules.cn.controllers import tipo_concepto_controller
from modules.cn.controllers import concepto_precio_controller
from modules.cn.controllers import unidad_concepto_controller
from modules.cn.controllers import forma_pago_controller
from modules.cn.controllers import cuota_controller


urlpatterns = [
    path('tipos-concepto/', tipo_concepto_controller.tipo_concepto_listar),
    path('tipos-concepto/<int:idtipo>/', tipo_concepto_controller.tipo_concepto_detalle),
    path('tipos-concepto/crear/', tipo_concepto_controller.tipo_concepto_crear),
    path('tipos-concepto/<int:idtipo>/actualizar/', tipo_concepto_controller.tipo_concepto_actualizar),
    path('tipos-concepto/<int:idtipo>/eliminar/', tipo_concepto_controller.tipo_concepto_eliminar),

    path('conceptos-precio/', concepto_precio_controller.concepto_precio_listar),
    path('conceptos-precio/<int:idconcepto>/', concepto_precio_controller.concepto_precio_detalle),
    path('conceptos-precio/crear/', concepto_precio_controller.concepto_precio_crear),
    path('conceptos-precio/<int:idconcepto>/actualizar/', concepto_precio_controller.concepto_precio_actualizar),
    path('conceptos-precio/<int:idconcepto>/eliminar/', concepto_precio_controller.concepto_precio_eliminar),

    path('unidad-conceptos/', unidad_concepto_controller.unidad_concepto_listar),
    path('unidad-conceptos/<int:id>/', unidad_concepto_controller.unidad_concepto_detalle),
    path('unidad-conceptos/crear/', unidad_concepto_controller.unidad_concepto_crear),
    path('unidad-conceptos/<int:id>/actualizar/', unidad_concepto_controller.unidad_concepto_actualizar),
    path('unidad-conceptos/<int:id>/eliminar/', unidad_concepto_controller.unidad_concepto_eliminar),
    path('unidad-conceptos/unidad/<int:idunidad>/', unidad_concepto_controller.unidad_concepto_por_unidad),

    path('formas-pago/', forma_pago_controller.forma_pago_listar),
    path('formas-pago/<int:idformapago>/', forma_pago_controller.forma_pago_detalle),
    path('formas-pago/crear/', forma_pago_controller.forma_pago_crear),
    path('formas-pago/<int:idformapago>/actualizar/', forma_pago_controller.forma_pago_actualizar),
    path('formas-pago/<int:idformapago>/eliminar/', forma_pago_controller.forma_pago_eliminar),

    path('cuotas/', cuota_controller.cuota_listar),
    path('cuotas/<int:idcuota>/', cuota_controller.cuota_detalle),
    path('cuotas/crear/', cuota_controller.cuota_crear),
    path('cuotas/<int:idcuota>/actualizar/', cuota_controller.cuota_actualizar),
    path('cuotas/<int:idcuota>/eliminar/', cuota_controller.cuota_eliminar),
    path('cuotas/<int:idcuota>/pagar/', cuota_controller.cuota_pagar),  # 🔴 NUEVO - CRÍTICO
]
