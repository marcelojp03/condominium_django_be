from rest_framework import serializers
from modules.ad.models.reserva_area_model import ReservaArea

class ReservaAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservaArea
        fields = [
            'idreserva', 'unidad', 'area', 'usuario_reserva',
            'fecha_reserva', 'hora_inicio', 'hora_fin',
            'motivo', 'estado'
        ]
