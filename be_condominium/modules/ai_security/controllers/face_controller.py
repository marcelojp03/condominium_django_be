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

    try:
        image_bytes = image_file.read()
        result = rekognition_service.search_face(image_bytes)
        match = result.get('FaceMatches', [])
    except Exception as e:
        # Manejo de errores de Rekognition
        error_message = str(e)
        if "ResourceNotFoundException" in error_message:
            return Response({
                "error": "Colección de rostros no configurada", 
                "details": "Ejecuta setup_rekognition_collections.py"
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        elif "InvalidImageException" in error_message:
            return Response({
                "error": "Imagen inválida o sin rostros detectables"
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "error": "Error en servicio de reconocimiento facial",
                "details": error_message
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

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

    # No match: registrar visitante desconocido
    try:
        index_result = rekognition_service.index_unknown_face(image_bytes)
        face_records = index_result.get('FaceRecords', [])
        if face_records:
            visitor_face_id = face_records[0]['Face']['FaceId']
            similarity = 0.0  # opcional, ya que no hay match
            UnknownVisitor.objects.create(
                image=image_file,
                face_id=visitor_face_id,
                similarity=similarity
            )
    except Exception as e:
        # Si falla indexar visitante desconocido, continuar sin error crítico
        print(f"Warning: No se pudo indexar visitante desconocido: {e}")

    event.save()
    return Response({"matched": False, "message": "Visitante no reconocido registrado"}, status=status.HTTP_200_OK)


