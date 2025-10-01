from rest_framework import serializers
from modules.ad.models.residente_foto_model import ResidenteFoto

class ResidenteFotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResidenteFoto
        fields = ['idfoto', 'residente', 'url_imagen', 'fecha_registro', 'tipo', 'estado']
