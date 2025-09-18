from django.urls import path
from modules.ad.controllers import usuario_controller

urlpatterns = [
    path('usuarios/', usuario_controller.listar_usuarios),
    path('usuarios/<int:usuario_id>/', usuario_controller.obtener_usuario),
    path('usuarios/crear/', usuario_controller.crear_usuario),
    path('usuarios/<int:usuario_id>/actualizar/', usuario_controller.actualizar_usuario),
    path('usuarios/<int:usuario_id>/eliminar/', usuario_controller.eliminar_usuario),
]
