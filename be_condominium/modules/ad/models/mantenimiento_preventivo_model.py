from django.db import models
from modules.ad.models.area_comun_model import AreaComun
from modules.ad.models.usuario import Usuario

class MantenimientoPreventivo(models.Model):
    idpreventivo = models.AutoField(primary_key=True)
    area = models.ForeignKey(AreaComun, on_delete=models.PROTECT)
    frecuencia = models.CharField(max_length=20)  # 'MENSUAL', 'TRIMESTRAL', etc.
    ultima_fecha = models.DateField(null=True, blank=True)
    estado = models.BooleanField(default=True)
    observaciones = models.TextField(null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    usuario_alta = models.ForeignKey(Usuario, on_delete=models.PROTECT)

    class Meta:
        db_table = 'ad_mantenimiento_preventivo'
        verbose_name = 'Mantenimiento Preventivo'
        verbose_name_plural = 'Mantenimientos Preventivos'

    def __str__(self):
        return f"{self.area.nombre} - {self.frecuencia}"
