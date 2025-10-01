from modules.ad.models.tipo_documento_model import TipoDocumentoIdentidad

class TipoDocumentoRepository:

    @staticmethod
    def listar():
        return TipoDocumentoIdentidad.objects.filter(estado=True).order_by('nombre')

    @staticmethod
    def obtener_por_id(idtipo):
        return TipoDocumentoIdentidad.objects.filter(idtipo_documento_identidad=idtipo).first()

    @staticmethod
    def crear(data):
        return TipoDocumentoIdentidad.objects.create(**data)

    @staticmethod
    def actualizar(idtipo, data):
        TipoDocumentoIdentidad.objects.filter(idtipo_documento_identidad=idtipo).update(**data)

    @staticmethod
    def eliminar(idtipo):
        TipoDocumentoIdentidad.objects.filter(idtipo_documento_identidad=idtipo).update(estado=False)
