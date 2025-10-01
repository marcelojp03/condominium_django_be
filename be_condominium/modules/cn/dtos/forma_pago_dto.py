from rest_framework import serializers
from modules.cn.models.forma_pago_model import FormaPago

class FormaPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormaPago
        fields = ['idformapago', 'nombre', 'descripcion', 'estado']
