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

]
