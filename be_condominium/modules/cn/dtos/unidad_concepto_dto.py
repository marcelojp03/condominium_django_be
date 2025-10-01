from rest_framework import serializers
from modules.cn.models.unidad_concepto_model import UnidadConcepto

class UnidadConceptoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadConcepto
        fields = ['id', 'unidad', 'concepto', 'fecha_asignacion', 'monto_personalizado', 'estado']
