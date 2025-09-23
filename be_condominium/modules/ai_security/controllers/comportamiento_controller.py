from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from modules.ai_security.services import rekognition_service
from modules.ai_security.models import VehicleAccessEvent,Vehicle,EventoSospechoso

@api_view(['POST'])
@parser_classes([MultiPartParser])
def escanear_comportamiento(request):
    imagen = request.FILES.get('imagen')
    if not imagen:
        return Response({"error": "No se envió imagen"}, status=status.HTTP_400_BAD_REQUEST)

    imagen_bytes = imagen.read()
    etiquetas = rekognition_service.detectar_comportamiento_sospechoso(imagen_bytes)

    eventos = []
    for etiqueta in etiquetas:
        nombre = etiqueta['Name']  # Ej: 'perro_suelto'
        confianza = etiqueta['Confidence']
        evento = EventoSospechoso.objects.create(
            imagen=imagen,
            tipo_evento=nombre,
            confianza=confianza,
            metadatos=etiqueta
        )
        eventos.append({
            "tipo_evento": nombre,
            "confianza": confianza
        })

    return Response({"eventos_detectados": eventos}, status=status.HTTP_201_CREATED)
