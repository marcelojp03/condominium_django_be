from django.urls import path
from modules.ad.controllers import usuario_controller
from modules.ad.controllers import recurso_controller
from modules.ad.controllers import rol_controller
from modules.ad.controllers import rol_recurso_controller
from modules.ad.controllers import subrecurso_controller
from modules.ad.controllers import usuario_rol_controller
from modules.ad.controllers import menu_controller
from modules.ad.controllers import auth_controller
from modules.ad.controllers import zona_controller
from modules.ad.controllers import unidad_controller
from modules.ad.controllers import tipo_documento_controller
from modules.ad.controllers import residente_controller
from modules.ad.controllers import residente_foto_controller
from modules.ad.controllers import vehiculo_controller
from modules.ad.controllers import vehiculo_foto_controller
from modules.ad.controllers import aviso_controller
from modules.ad.controllers import area_comun_controller
from modules.ad.controllers import reserva_area_controller
from modules.ad.controllers import tarea_mantenimiento_controller
from modules.ad.controllers import mantenimiento_preventivo_controller
# 🟠🟢 NUEVOS CONTROLLERS FASE 2 y 3
from modules.ad.controllers import residente_perfil_controller
from modules.ad.controllers import dashboard_controller
from modules.ad.controllers import notificaciones_controller


urlpatterns = [
    path('usuarios/', usuario_controller.listar_usuarios),
    path('usuarios/<int:usuario_id>/', usuario_controller.obtener_usuario),
    path('usuarios/crear/', usuario_controller.crear_usuario),
    path('usuarios/<int:usuario_id>/actualizar/', usuario_controller.actualizar_usuario),
    path('usuarios/<int:usuario_id>/eliminar/', usuario_controller.eliminar_usuario),

    path('roles/', rol_controller.rol_listar_crear),
    path('roles/<int:pk>/', rol_controller.rol_detalle),
    path('roles/recursos/<int:pk>/', rol_controller.rol_detalle_recursos),

    path('usuarios-roles/', usuario_rol_controller.usuario_rol_listar_crear),

    path('recursos/', recurso_controller.recurso_listar_crear),
    path('subrecursos/', subrecurso_controller.subrecurso_listar_crear),
    path('roles-recursos/', rol_recurso_controller.rol_recurso_listar_crear),

    path('menu/<int:usuario_id>/', menu_controller.obtener_menu_por_usuario),
    path('auth/login', auth_controller.login),

    path('zonas/', zona_controller.zona_listar),
    path('zonas/<int:idzona>/', zona_controller.zona_detalle),
    path('zonas/crear/', zona_controller.zona_crear),
    path('zonas/<int:idzona>/actualizar/', zona_controller.zona_actualizar),
    path('zonas/<int:idzona>/eliminar/', zona_controller.zona_eliminar),


    path('unidades/', unidad_controller.unidad_listar),
    path('unidades/<int:idunidad>/', unidad_controller.unidad_detalle),
    path('unidades/crear/', unidad_controller.unidad_crear),
    path('unidades/<int:idunidad>/actualizar/', unidad_controller.unidad_actualizar),
    path('unidades/<int:idunidad>/eliminar/', unidad_controller.unidad_eliminar),


    path('tipos-documento/', tipo_documento_controller.tipo_documento_listar),
    path('tipos-documento/<int:idtipo>/', tipo_documento_controller.tipo_documento_detalle),
    path('tipos-documento/crear/', tipo_documento_controller.tipo_documento_crear),
    path('tipos-documento/<int:idtipo>/actualizar/', tipo_documento_controller.tipo_documento_actualizar),
    path('tipos-documento/<int:idtipo>/eliminar/', tipo_documento_controller.tipo_documento_eliminar),

    path('residentes/', residente_controller.residente_listar),
    path('residentes/<int:idresidente>/', residente_controller.residente_detalle),
    path('residentes/crear/', residente_controller.residente_crear),
    path('residentes/<int:idresidente>/actualizar/', residente_controller.residente_actualizar),
    path('residentes/<int:idresidente>/eliminar/', residente_controller.residente_eliminar),

    path('residentes/fotos/', residente_foto_controller.residente_foto_listar),
    path('residentes/fotos/<int:idfoto>/', residente_foto_controller.residente_foto_detalle),
    path('residentes/fotos/crear/', residente_foto_controller.residente_foto_crear),
    path('residentes/fotos/<int:idfoto>/actualizar/', residente_foto_controller.residente_foto_actualizar),
    path('residentes/fotos/<int:idfoto>/eliminar/', residente_foto_controller.residente_foto_eliminar),

    path('vehiculos/', vehiculo_controller.vehiculo_listar),
    path('vehiculos/<int:idvehiculo>/', vehiculo_controller.vehiculo_detalle),
    path('vehiculos/crear/', vehiculo_controller.vehiculo_crear),
    path('vehiculos/<int:idvehiculo>/actualizar/', vehiculo_controller.vehiculo_actualizar),
    path('vehiculos/<int:idvehiculo>/eliminar/', vehiculo_controller.vehiculo_eliminar),

    path('vehiculos/fotos/', vehiculo_foto_controller.vehiculo_foto_listar),
    path('vehiculos/fotos/<int:idfoto>/', vehiculo_foto_controller.vehiculo_foto_detalle),
    path('vehiculos/fotos/crear/', vehiculo_foto_controller.vehiculo_foto_crear),
    path('vehiculos/fotos/<int:idfoto>/actualizar/', vehiculo_foto_controller.vehiculo_foto_actualizar),
    path('vehiculos/fotos/<int:idfoto>/eliminar/', vehiculo_foto_controller.vehiculo_foto_eliminar),

    path('avisos/', aviso_controller.aviso_listar),
    path('avisos/<int:idaviso>/', aviso_controller.aviso_detalle),
    path('avisos/crear/', aviso_controller.aviso_crear),
    path('avisos/<int:idaviso>/actualizar/', aviso_controller.aviso_actualizar),
    path('avisos/<int:idaviso>/eliminar/', aviso_controller.aviso_eliminar),

    path('areas-comunes/', area_comun_controller.area_comun_listar),
    path('areas-comunes/<int:idarea>/', area_comun_controller.area_comun_detalle),
    path('areas-comunes/crear/', area_comun_controller.area_comun_crear),
    path('areas-comunes/<int:idarea>/actualizar/', area_comun_controller.area_comun_actualizar),
    path('areas-comunes/<int:idarea>/eliminar/', area_comun_controller.area_comun_eliminar),


    path('reservas-area/', reserva_area_controller.reserva_area_listar),
    path('reservas-area/<int:idreserva>/', reserva_area_controller.reserva_area_detalle),
    path('reservas-area/crear/', reserva_area_controller.reserva_area_crear),
    path('reservas-area/<int:idreserva>/actualizar/', reserva_area_controller.reserva_area_actualizar),
    path('reservas-area/<int:idreserva>/eliminar/', reserva_area_controller.reserva_area_eliminar),    

    path('tareas-mantenimiento/', tarea_mantenimiento_controller.tarea_mantenimiento_listar),
    path('tareas-mantenimiento/<int:idtarea>/', tarea_mantenimiento_controller.tarea_mantenimiento_detalle),
    path('tareas-mantenimiento/crear/', tarea_mantenimiento_controller.tarea_mantenimiento_crear),
    path('tareas-mantenimiento/<int:idtarea>/actualizar/', tarea_mantenimiento_controller.tarea_mantenimiento_actualizar),
    path('tareas-mantenimiento/<int:idtarea>/eliminar/', tarea_mantenimiento_controller.tarea_mantenimiento_eliminar),

    path('mantenimientos-preventivos/', mantenimiento_preventivo_controller.mantenimiento_preventivo_listar),
    path('mantenimientos-preventivos/<int:idpreventivo>/', mantenimiento_preventivo_controller.mantenimiento_preventivo_detalle),
    path('mantenimientos-preventivos/crear/', mantenimiento_preventivo_controller.mantenimiento_preventivo_crear),
    path('mantenimientos-preventivos/<int:idpreventivo>/actualizar/', mantenimiento_preventivo_controller.mantenimiento_preventivo_actualizar),
    path('mantenimientos-preventivos/<int:idpreventivo>/eliminar/', mantenimiento_preventivo_controller.mantenimiento_preventivo_eliminar),    

    # 🟡 NUEVOS ENDPOINTS FASE 2 - IMPORTANTES
    path('residentes/mis-datos/<int:usuario_id>/', residente_perfil_controller.residente_mis_datos),
    
    # 🟢 NUEVOS ENDPOINTS FASE 3 - OPCIONALES
    path('dashboard/residente/<int:residente_id>/', dashboard_controller.dashboard_residente),
    path('dashboard/guardia/', dashboard_controller.dashboard_guardia),
    
    # 🟢 SISTEMA DE NOTIFICACIONES
    path('notificaciones/push/', notificaciones_controller.enviar_notificacion_push),
    path('notificaciones/registrar-token/', notificaciones_controller.registrar_token_dispositivo),

]
