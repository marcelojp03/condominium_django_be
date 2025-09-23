from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from modules.ai_security.services import rekognition_service
from modules.ai_security.models import VehicleAccessEvent,Vehicle

@api_view(['POST'])
@parser_classes([MultiPartParser])
def escanear_placa(request):
    image_file = request.FILES.get('image')
    if not image_file:
        return Response({"error": "No se envió imagen"}, status=status.HTTP_400_BAD_REQUEST)

    image_bytes = image_file.read()
    plate_texts = rekognition_service.detect_plate_text(image_bytes)

    for t in plate_texts:
        plate = t['DetectedText']
        confidence = t['Confidence']
        if rekognition_service.is_valid_plate(plate):
            # 🔗 Buscar si la placa está registrada
            try:
                vehicle = Vehicle.objects.get(plate_number=plate)
                matched_resident = vehicle.owner
            except Vehicle.DoesNotExist:
                matched_resident = None

            # ✅ Crear evento con vinculación
            event = VehicleAccessEvent.objects.create(
                image=image_file,
                plate_number=plate,
                confidence=confidence,
                placa_valida=True,
                matched_resident=matched_resident
            )

            return Response({
                "matched": True,
                "plate_number": plate,
                "confidence": confidence,
                "resident_id": matched_resident.id if matched_resident else None,
                "resident_name": str(matched_resident) if matched_resident else None

            }, status=status.HTTP_201_CREATED)

    return Response({
        "matched": False,
        "message": "No se detectó placa válida"
    }, status=status.HTTP_200_OK)