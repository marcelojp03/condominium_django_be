from modules.ad.models.residente_foto_model import ResidenteFoto

class ResidenteFotoRepository:

    @staticmethod
    def listar():
        return ResidenteFoto.objects.filter(estado=True).order_by('-fecha_registro')

    @staticmethod
    def obtener_por_id(idfoto):
        return ResidenteFoto.objects.filter(idfoto=idfoto).first()

    @staticmethod
    def crear(data):
        return ResidenteFoto.objects.create(**data)

    @staticmethod
    def actualizar(idfoto, data):
        ResidenteFoto.objects.filter(idfoto=idfoto).update(**data)

    @staticmethod
    def eliminar(idfoto):
        ResidenteFoto.objects.filter(idfoto=idfoto).update(estado=False)

    @staticmethod
    def obtener_por_face_id(face_id):
        return ResidenteFoto.objects.filter(rekognition_face_id=face_id, estado=True).first()