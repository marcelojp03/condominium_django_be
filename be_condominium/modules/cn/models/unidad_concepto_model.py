from django.db import models
from modules.ad.models.unidad_model import Unidad
from modules.cn.models.concepto_precio_model import ConceptoPrecio

class UnidadConcepto(models.Model):
    id = models.AutoField(primary_key=True)
    unidad = models.ForeignKey(Unidad, on_delete=models.PROTECT)
    concepto = models.ForeignKey(ConceptoPrecio, on_delete=models.PROTECT)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    monto_personalizado = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 'cn_unidad_concepto'
        verbose_name = 'Concepto Asignado a Unidad'
        verbose_name_plural = 'Conceptos por Unidad'

    def __str__(self):
        return f"{self.unidad.codigo} → {self.concepto.nombre}"
