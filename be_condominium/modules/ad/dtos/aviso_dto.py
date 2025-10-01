from rest_framework import serializers
from modules.ad.models.aviso_model import Aviso

class AvisoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aviso
        fields = [
            'idaviso', 'fecha_alta', 'usuario_alta',
            'titulo', 'contenido', 'fecha_publicacion', 'estado'
        ]
