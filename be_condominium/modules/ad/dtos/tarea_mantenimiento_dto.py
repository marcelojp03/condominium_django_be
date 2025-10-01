from rest_framework import serializers
from modules.ad.models.tarea_mantenimiento_model import TareaMantenimiento

class TareaMantenimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TareaMantenimiento
        fields = [
            'idtarea', 'descripcion', 'responsable', 'tipo',
            'fecha_programada', 'fecha_ejecucion', 'estado',
            'costo', 'observaciones', 'fecha_registro', 'usuario_alta'
        ]
