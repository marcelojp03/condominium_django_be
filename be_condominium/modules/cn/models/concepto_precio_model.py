from django.db import models
from modules.ad.models.usuario import Usuario
from modules.cn.models.tipo_concepto_model import TipoConcepto

class ConceptoPrecio(models.Model):
    idconcepto = models.AutoField(primary_key=True)
    fecha_alta = models.DateTimeField(auto_now_add=True)
    usuario_alta = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    tipo_concepto = models.ForeignKey(TipoConcepto, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    vigente_desde = models.DateField()
    vigente_hasta = models.DateField(null=True, blank=True)
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 'cn_concepto_precio'
        verbose_name = 'Concepto con Precio'
        verbose_name_plural = 'Conceptos con Precio'

    def __str__(self):
        return self.nombre
