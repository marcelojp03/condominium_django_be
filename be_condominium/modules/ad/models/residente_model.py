from django.db import models
from modules.ad.models.unidad_model import Unidad
from modules.ad.models.usuario import Usuario
from modules.ad.models.tipo_documento_model import TipoDocumentoIdentidad

class Residente(models.Model):
    idresidente = models.AutoField(primary_key=True)
    unidad = models.ForeignKey(Unidad, on_delete=models.PROTECT)
    fecha_alta = models.DateTimeField(auto_now_add=True)
    usuario_alta = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    nombres = models.CharField(max_length=100)
    apellido1 = models.CharField(max_length=50)
    apellido2 = models.CharField(max_length=50)
    tipo_documento = models.ForeignKey(TipoDocumentoIdentidad, on_delete=models.PROTECT)
    numero_documento = models.CharField(max_length=50)
    extension_documento = models.CharField(max_length=10, null=True, blank=True)
    correo_electronico = models.EmailField(max_length=100, null=True, blank=True)
    relacion = models.CharField(max_length=50)  # PROPIETARIO, INQUILINO, FAMILIAR
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 'ad_residente'
        verbose_name = 'Residente'
        verbose_name_plural = 'Residentes'

    def __str__(self):
        return f"{self.nombres} {self.apellido1}"
