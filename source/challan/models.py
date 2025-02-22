from django.db import models

class Violation(models.Model):
    number_plate = models.CharField(max_length=20)
    violation_time = models.CharField(max_length =20)
    fine_amount = models.IntegerField(default=500)
    image = models.CharField(max_length=300)  # Store the directory path



    def __str__(self):
        return self.number_plate
