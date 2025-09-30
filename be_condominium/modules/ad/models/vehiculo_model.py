from django.db import models
from modules.ad.models.unidad_model import Unidad

class Vehiculo(models.Model):
    idvehiculo = models.AutoField(primary_key=True)
    unidad = models.ForeignKey(Unidad, on_delete=models.PROTECT)
    marca = models.CharField(max_length=50, null=True, blank=True)
    modelo = models.CharField(max_length=50, null=True, blank=True)
    color = models.CharField(max_length=30, null=True, blank=True)
    placa = models.CharField(max_length=20)
    estado = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ad_vehiculo'
        verbose_name = 'Vehículo'
        verbose_name_plural = 'Vehículos'

    def __str__(self):
        return f"{self.placa} ({self.unidad.codigo})"
