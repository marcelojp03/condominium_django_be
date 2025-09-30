from rest_framework import serializers
from modules.ad.models.unidad_model import Unidad

class UnidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unidad
        fields = ['idunidad', 'fecha_alta', 'usuario_alta', 'codigo', 'zona', 'estado']
