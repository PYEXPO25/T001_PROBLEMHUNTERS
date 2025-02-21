from django.db import models

class Violation(models.Model):
    number_plate = models.CharField(max_length=20)
    violation_time = models.CharField(max_length =20)
    fine_amount = models.IntegerField(default=500)
    image = models.ImageField(upload_to='violations/', blank=True, null=True)

    def __str__(self):
        return f"{self.number_plate} - {self.violation_time}"
