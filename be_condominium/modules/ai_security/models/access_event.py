from django.db import models
from .resident import Resident
from modules.ad.models.residente_model import Residente

class AccessEvent(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='access_events/')
    #matched_resident = models.ForeignKey(Resident, null=True, blank=True, on_delete=models.SET_NULL)
    matched_resident = models.ForeignKey(Residente, on_delete=models.PROTECT, null=True)
    confidence = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.timestamp} - {self.matched_resident or 'Desconocido'}"
