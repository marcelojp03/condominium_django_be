from rest_framework import serializers
from modules.ad.models.zona_model import Zona

class ZonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zona
        fields = ['idzona', 'nombre', 'descripcion', 'estado']
