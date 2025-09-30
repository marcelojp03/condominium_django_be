from django.db import models
from modules.ad.models.usuario import Usuario

class Aviso(models.Model):
    idaviso = models.AutoField(primary_key=True)
    fecha_alta = models.DateTimeField(auto_now_add=True)
    usuario_alta = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    fecha_publicacion = models.DateField()
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 'ad_aviso'
        verbose_name = 'Aviso'
        verbose_name_plural = 'Avisos'

    def __str__(self):
        return self.titulo
