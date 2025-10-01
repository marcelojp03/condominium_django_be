import boto3,re

rekognition = boto3.client('rekognition')
PROJECT_VERSION_ARN = 'arn:aws:rekognition:us-east-1:851725478821:project/ComportamientoSospechoso/version/ComportamientoSospechoso.2025-09-21T20.10.36/1758499835614'
def index_face_s3(bucket, image_key, resident_id):
    response = rekognition.index_faces(
        CollectionId='residentes-condominio',
        Image={'S3Object': {'Bucket': bucket, 'Name': image_key}},
        ExternalImageId=str(resident_id),
        DetectionAttributes=['DEFAULT']
    )
    return response

def search_face(image_bytes):

    response_aux = rekognition.list_faces(CollectionId='residentes-condominio')
    print("response-aux:" + str(response_aux))

    response = rekognition.search_faces_by_image(
        CollectionId='residentes-condominio',
        Image={'Bytes': image_bytes},
        MaxFaces=1,
        FaceMatchThreshold=85
    )
    return response    

def index_unknown_face(image_bytes):
    response = rekognition.index_faces(
        CollectionId='visitantes-condominio',
        Image={'Bytes': image_bytes},
        DetectionAttributes=['DEFAULT']
    )
    return response   

def detect_plate_text(image_bytes):
    response = rekognition.detect_text(Image={'Bytes': image_bytes})
    texts = response['TextDetections']

    # Filtrar por tamaño y posición (placas suelen estar centradas y horizontales)
    filtered = []
    for t in texts:
        box = t['Geometry']['BoundingBox']
        if box['Width'] > 0.2 and box['Height'] < 0.2:  # ancho suficiente, altura baja
            filtered.append(t)

    return filtered

def is_valid_plate(text):
    pattern = r'^[0-9]{3,4}[A-Z]{2,3}$'  # Ej: 2809LEU
    return re.match(pattern, text) is not None

def detectar_comportamiento_sospechoso(imagen_bytes):
    response = rekognition.detect_custom_labels(
        ProjectVersionArn=PROJECT_VERSION_ARN,
        Image={'Bytes': imagen_bytes},
        MinConfidence=70
    )
    return response.get('CustomLabels', [])
