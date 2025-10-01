from rest_framework import serializers
from modules.cn.models.cuota_model import Cuota

class CuotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuota
        fields = [
            'idcuota', 'unidad', 'concepto', 'periodo',
            'fecha_generacion', 'monto', 'estado_pago',
            'fecha_pago', 'forma_pago', 'observaciones'
        ]
