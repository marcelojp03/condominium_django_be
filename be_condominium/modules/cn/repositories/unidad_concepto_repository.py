from modules.cn.models.unidad_concepto_model import UnidadConcepto

class UnidadConceptoRepository:

    @staticmethod
    def listar():
        return UnidadConcepto.objects.filter(estado=True).order_by('-fecha_asignacion')

    @staticmethod
    def obtener_por_id(id):
        return UnidadConcepto.objects.filter(id=id).first()

    @staticmethod
    def crear(data):
        return UnidadConcepto.objects.create(**data)

    @staticmethod
    def actualizar(id, data):
        UnidadConcepto.objects.filter(id=id).update(**data)

    @staticmethod
    def eliminar(id):
        UnidadConcepto.objects.filter(id=id).update(estado=False)
