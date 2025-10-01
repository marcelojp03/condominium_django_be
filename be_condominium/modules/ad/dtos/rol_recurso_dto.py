from rest_framework import serializers
from ..models.rol_recurso import RolRecurso

class RolRecursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolRecurso
        fields = '__all__'
