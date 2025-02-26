
from django.db import models

class Violation(models.Model):
    
    number_plate = models.CharField(max_length=20)
    violation_time = models.DateTimeField(auto_now_add=True)
    fine_amount = models.IntegerField(default=500)
    image = models.CharField(max_length=300)
    status=models.CharField(max_length=20,default='Not Paid')



    def __str__(self):
        return self.number_plate