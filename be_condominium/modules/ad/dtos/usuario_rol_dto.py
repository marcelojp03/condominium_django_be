from rest_framework import serializers
from ..models.usuario_rol import UsuarioRol

class UsuarioRolSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioRol
        fields = '__all__'
