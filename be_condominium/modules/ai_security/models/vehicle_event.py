from django.db import models
from .resident import Resident

class VehicleAccessEvent(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='vehicle_events/')
    plate_number = models.CharField(max_length=20)
    confidence = models.FloatField()
    matched_resident = models.ForeignKey(Resident, null=True, blank=True, on_delete=models.SET_NULL)
    placa_valida = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.timestamp} - {self.plate_number}"
