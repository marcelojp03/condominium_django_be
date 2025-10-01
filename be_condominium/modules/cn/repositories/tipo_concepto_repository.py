from modules.cn.models.tipo_concepto_model import TipoConcepto

class TipoConceptoRepository:

    @staticmethod
    def listar():
        return TipoConcepto.objects.filter(estado=True).order_by('nombre')

    @staticmethod
    def obtener_por_id(idtipo):
        return TipoConcepto.objects.filter(idtipo_concepto=idtipo).first()

    @staticmethod
    def crear(data):
        return TipoConcepto.objects.create(**data)

    @staticmethod
    def actualizar(idtipo, data):
        TipoConcepto.objects.filter(idtipo_concepto=idtipo).update(**data)

    @staticmethod
    def eliminar(idtipo):
        TipoConcepto.objects.filter(idtipo_concepto=idtipo).update(estado=False)
