from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Plan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    duration = models.PositiveIntegerField()  # Duration in months
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    


class PurchasePlan(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan,on_delete=models.CASCADE)
