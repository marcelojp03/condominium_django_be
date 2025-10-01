from django.db import models
from modules.ad.models.area_comun_model import AreaComun
from modules.ad.models.unidad_model import Unidad
from modules.ad.models.usuario import Usuario

class ReservaArea(models.Model):
    idreserva = models.AutoField(primary_key=True)
    unidad = models.ForeignKey(Unidad, on_delete=models.PROTECT)
    area = models.ForeignKey(AreaComun, on_delete=models.PROTECT)
    usuario_reserva = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    fecha_reserva = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    motivo = models.TextField(null=True, blank=True)
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 'ad_reserva_area'
        verbose_name = 'Reserva de Área Común'
        verbose_name_plural = 'Reservas de Áreas Comunes'

    def __str__(self):
        return f"{self.area.nombre} - {self.fecha_reserva} ({self.hora_inicio}–{self.hora_fin})"
