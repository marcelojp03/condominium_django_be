from modules.cn.models.concepto_precio_model import ConceptoPrecio

class ConceptoPrecioRepository:

    @staticmethod
    def listar():
        return ConceptoPrecio.objects.filter(estado=True).order_by('-vigente_desde')

    @staticmethod
    def obtener_por_id(idconcepto):
        return ConceptoPrecio.objects.filter(idconcepto=idconcepto).first()

    @staticmethod
    def crear(data):
        return ConceptoPrecio.objects.create(**data)

    @staticmethod
    def actualizar(idconcepto, data):
        ConceptoPrecio.objects.filter(idconcepto=idconcepto).update(**data)

    @staticmethod
    def eliminar(idconcepto):
        ConceptoPrecio.objects.filter(idconcepto=idconcepto).update(estado=False)
