from rest_framework import serializers
from modules.ad.models.vehiculo_foto_model import VehiculoFoto

class VehiculoFotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehiculoFoto
        fields = ['idfoto', 'vehiculo', 'url_imagen', 'fecha_registro', 'tipo', 'estado']
