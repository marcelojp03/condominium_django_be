from rest_framework import serializers
from modules.cn.models.tipo_concepto_model import TipoConcepto

class TipoConceptoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoConcepto
        fields = ['idtipo_concepto', 'nombre', 'descripcion', 'estado']
