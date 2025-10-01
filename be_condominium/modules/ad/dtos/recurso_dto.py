from rest_framework import serializers
from ..models.recurso import Recurso
from ..models.subrecurso import Subrecurso
from modules.ad.dtos.subrecurso_dto import SubrecursoSerializer
class RecursoSerializer(serializers.ModelSerializer):
    subrecursos = serializers.SerializerMethodField()
    class Meta:
        model = Recurso
        fields = '__all__'

    def get_subrecursos(self, obj):
        subrecursos = Subrecurso.objects.filter(recurso=obj)
        return SubrecursoSerializer(subrecursos, many=True).data
