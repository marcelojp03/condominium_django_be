from rest_framework import serializers
from modules.ad.models.mantenimiento_preventivo_model import MantenimientoPreventivo

class MantenimientoPreventivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MantenimientoPreventivo
        fields = [
            'idpreventivo', 'area', 'frecuencia', 'ultima_fecha',
            'estado', 'observaciones', 'fecha_registro', 'usuario_alta'
        ]
