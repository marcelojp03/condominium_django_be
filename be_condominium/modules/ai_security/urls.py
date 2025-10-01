from django.urls import path
from modules.ai_security.controllers import (
    face_controller, 
    vehicle_controller,
    comportamiento_controller,
    eventos_acceso_controller,
    eventos_sospechosos_controller
)

urlpatterns = [
    path('registrar-rostro/', face_controller.registrar_rostro),
    path('escanear-rostro/', face_controller.escanear_rostro),
    path('escanear-placa/', vehicle_controller.escanear_placa),
    path('escanear-comportamiento/', comportamiento_controller.escanear_comportamiento),
    
    # 🟠 NUEVOS ENDPOINTS FASE 2
    path('eventos-acceso/', eventos_acceso_controller.eventos_acceso_listar),
    path('registrar-evento-manual/', eventos_acceso_controller.registrar_evento_manual),
    
    # 🟢 NUEVOS ENDPOINTS FASE 3
    path('eventos-sospechosos/', eventos_sospechosos_controller.eventos_sospechosos_listar),
    path('eventos-sospechosos/<int:id>/atender/', eventos_sospechosos_controller.evento_sospechoso_atender),
]
