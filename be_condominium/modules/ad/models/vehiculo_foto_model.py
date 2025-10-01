from django.db import models
from modules.ad.models.vehiculo_model import Vehiculo

class VehiculoFoto(models.Model):
    idfoto = models.AutoField(primary_key=True)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    url_imagen = models.TextField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=20, null=True, blank=True)  # 'PLACA_DELANTERA', 'PLACA_TRASERA', 'GENERAL'
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 'ad_vehiculo_foto'
        verbose_name = 'Foto de Vehículo'
        verbose_name_plural = 'Fotos de Vehículos'

    def __str__(self):
        return f"Foto {self.idfoto} - {self.vehiculo.placa}"
