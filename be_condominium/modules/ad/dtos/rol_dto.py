from rest_framework import serializers
from ..models.rol import Rol
from ..models.recurso import Recurso
from ..models.subrecurso import Subrecurso
from ..models.rol_recurso import RolRecurso

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'

class SubrecursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subrecurso
        fields = ['id', 'nombre', 'descripcion', 'url']

class RecursoConSubrecursosSerializer(serializers.ModelSerializer):
    subrecursos = serializers.SerializerMethodField()

    class Meta:
        model = Recurso
        fields = ['id', 'nombre', 'descripcion', 'subrecursos']

    def get_subrecursos(self, recurso):
        rol = self.context.get('rol')
        subrecursos = Subrecurso.objects.filter(
            rolrecurso__rol=rol,
            rolrecurso__recurso=recurso
        )
        return SubrecursoSerializer(subrecursos, many=True).data

class RolDetalleSerializer(serializers.ModelSerializer):
    recursos = serializers.SerializerMethodField()

    class Meta:
        model = Rol
        fields = ['id', 'nombre', 'descripcion', 'estado', 'recursos']

    def get_recursos(self, rol):
        recursos = Recurso.objects.filter(rolrecurso__rol=rol).distinct()
        return RecursoConSubrecursosSerializer(recursos, many=True, context={'rol': rol}).data