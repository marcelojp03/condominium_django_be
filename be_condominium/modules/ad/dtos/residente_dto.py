from rest_framework import serializers
from modules.ad.models.residente_model import Residente

class ResidenteSerializer(serializers.ModelSerializer):
    codigo_unidad = serializers.SerializerMethodField()
    class Meta:
        model = Residente
        fields = [
            'idresidente', 'unidad', 'fecha_alta', 'usuario_alta',
            'nombres', 'apellido1', 'apellido2',
            'tipo_documento', 'numero_documento', 'extension_documento',
            'correo_electronico', 'relacion', 'estado','codigo_unidad' 
        ]
    def get_codigo_unidad(self, obj):
        return obj.unidad.codigo if obj.unidad else None    
