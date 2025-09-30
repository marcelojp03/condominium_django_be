from django.db import models
from modules.ad.models.zona_model import Zona
from modules.ad.models.usuario import Usuario  

class Unidad(models.Model):
    idunidad = models.AutoField(primary_key=True)
    fecha_alta = models.DateTimeField(auto_now_add=True)
    usuario_alta = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    codigo = models.CharField(max_length=20)
    zona = models.ForeignKey(Zona, on_delete=models.PROTECT)
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 'ad_unidad'
        verbose_name = 'Unidad Habitacional'
        verbose_name_plural = 'Unidades Habitacionales'

    def __str__(self):
        return f"{self.codigo} ({self.zona.nombre})"
