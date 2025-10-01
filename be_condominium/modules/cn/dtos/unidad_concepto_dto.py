from rest_framework import serializers
from modules.cn.models.unidad_concepto_model import UnidadConcepto

class UnidadConceptoSerializer(serializers.ModelSerializer):
    codigo_unidad = serializers.SerializerMethodField()
    nombre_concepto = serializers.SerializerMethodField()

    class Meta:
        model = UnidadConcepto
        fields = [
            'id', 'unidad', 'concepto', 'estado', 'monto_personalizado',
            'codigo_unidad', 'nombre_concepto'
        ]

    def get_codigo_unidad(self, obj):
        return obj.unidad.codigo if obj.unidad else None

    def get_nombre_concepto(self, obj):
        return obj.concepto.nombre if obj.concepto else None
