from django.urls import path
from modules.ai_security.controllers import face_controller, vehicle_controller,comportamiento_controller

urlpatterns = [
    path('registrar-rostro/', face_controller.registrar_rostro),
    path('escanear-rostro/', face_controller.escanear_rostro),
    path('escanear-placa/', vehicle_controller.escanear_placa),
    path('escanear-comportamiento/', comportamiento_controller.escanear_comportamiento),

]
