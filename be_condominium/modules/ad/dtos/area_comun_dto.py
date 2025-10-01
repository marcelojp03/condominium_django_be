from rest_framework import serializers
from modules.ad.models.area_comun_model import AreaComun

class AreaComunSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaComun
        fields = [
            'idarea', 'nombre', 'descripcion', 'capacidad',
            'horario_inicio', 'horario_fin', 'estado'
        ]
