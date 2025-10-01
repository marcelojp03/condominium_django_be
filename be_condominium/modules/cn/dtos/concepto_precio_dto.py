from rest_framework import serializers
from modules.cn.models.concepto_precio_model import ConceptoPrecio

class ConceptoPrecioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConceptoPrecio
        fields = [
            'idconcepto', 'fecha_alta', 'usuario_alta', 'tipo_concepto',
            'nombre', 'descripcion', 'monto', 'vigente_desde', 'vigente_hasta', 'estado'
        ]
