from django.db import models
from modules.ad.models.unidad_model import Unidad
from modules.cn.models.concepto_precio_model import ConceptoPrecio
from modules.cn.models.forma_pago_model import FormaPago

class Cuota(models.Model):
    idcuota = models.AutoField(primary_key=True)
    unidad = models.ForeignKey(Unidad, on_delete=models.PROTECT)
    concepto = models.ForeignKey(ConceptoPrecio, on_delete=models.PROTECT)
    periodo = models.CharField(max_length=7)  # formato 'YYYY-MM'
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    estado_pago = models.CharField(max_length=20, default='PENDIENTE')
    fecha_pago = models.DateTimeField(null=True, blank=True)
    forma_pago = models.ForeignKey(FormaPago, on_delete=models.SET_NULL, null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'cn_cuota'
        verbose_name = 'Cuota'
        verbose_name_plural = 'Cuotas'

    def __str__(self):
        return f"{self.periodo} - {self.unidad.codigo} - {self.concepto.nombre}"
