from django.db import models
from .resident import Resident

class Vehicle(models.Model):
    plate_number = models.CharField(max_length=20, unique=True)
    owner = models.ForeignKey(Resident, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.plate_number} - {self.owner.full_name}"
