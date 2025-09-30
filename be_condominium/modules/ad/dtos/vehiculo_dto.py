from rest_framework import serializers
from modules.ad.models.vehiculo_model import Vehiculo

class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = [
            'idvehiculo', 'unidad', 'marca', 'modelo',
            'color', 'placa', 'estado', 'fecha_registro'
        ]
