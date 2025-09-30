from rest_framework import serializers
from modules.ad.models.tipo_documento_model import TipoDocumentoIdentidad

class TipoDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDocumentoIdentidad
        fields = ['idtipo_documento_identidad', 'nombre', 'descripcion', 'estado']
