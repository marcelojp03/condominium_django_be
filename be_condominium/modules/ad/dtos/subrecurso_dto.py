from rest_framework import serializers
from ..models.subrecurso import Subrecurso

class SubrecursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subrecurso
        fields = '__all__'
