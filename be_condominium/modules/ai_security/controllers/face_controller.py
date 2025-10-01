from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from modules.ai_security.services import rekognition_service
from modules.ai_security.models import Resident, AccessEvent,UnknownVisitor
from modules.ad.repositories.residente_foto_repository import ResidenteFotoRepository

@api_view(['POST'])
def registrar_rostro(request):
    resident_id = request.data.get('resident_id')
    image_key = request.data.get('image_key')  # Ej: faces/sena.jpg
    bucket = 'vpay-paybox-bucket'

    if not resident_id or not image_key:
        return Response({"error": "Faltan datos"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        resident = Resident.objects.get(id=resident_id)
    except Resident.DoesNotExist:
        return Response({"error": "Residente no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    result = rekognition_service.index_face_s3(bucket, image_key, resident_id)
    face_records = result.get('FaceRecords', [])

    if face_records:
        face_id = face_records[0]['Face']['FaceId']
        resident.rekognition_face_id = face_id
        resident.save()
        return Response({"mensaje": "Rostro registrado", "face_id": face_id}, status=status.HTTP_201_CREATED)
    else:
        return Response({"error": "No se detectó rostro"}, status=status.HTTP_400_BAD_REQUEST)



from modules.ai_security.models import UnknownVisitor  # asegúrate de importar

@api_view(['POST'])
@parser_classes([MultiPartParser])
def escanear_rostro(request):
    image_file = request.FILES.get('image')
    if not image_file:
        return Response({"error": "No se envió imagen"}, status=status.HTTP_400_BAD_REQUEST)

    image_bytes = image_file.read()

    result = rekognition_service.search_face(image_bytes)
    match = result.get('FaceMatches', [])

    event = AccessEvent(image=image_file)

    if match:
        face_id = match[0]['Face']['FaceId']
        confidence = match[0]['Similarity']

        residente_foto = ResidenteFotoRepository.obtener_por_face_id(face_id)

        if residente_foto:
            residente = residente_foto.residente
            event.matched_resident = residente  # ✅ ahora funciona
            event.confidence = confidence
            event.save()

            return Response({
                "matched": True,
                "resident": f"{residente.nombres} {residente.apellido1} {residente.apellido2}",
                "confidence": confidence,
                "foto": residente_foto.url_imagen
            }, status=status.HTTP_200_OK)

    # No match
    index_result = rekognition_service.index_unknown_face(image_bytes)
    face_records = index_result.get('FaceRecords', [])
    if face_records:
        visitor_face_id = face_records[0]['Face']['FaceId']
        UnknownVisitor.objects.create(
            image=image_file,
            face_id=visitor_face_id,
            similarity=0.0
        )

    event.save()
    return Response({"matched": False}, status=status.HTTP_200_OK)