from django.db import models

# Create your models here.
class BeamModel(models.Model):
    len=models.FloatField()
    unit_1=models.CharField(max_length=4)
    f=models.FloatField()
    ft=models.FloatField()
    w=models.FloatField()
    wt=models.FloatField()
    unit_2=models.CharField(max_length=4)

class SupportModel(models.Model):
    a=models.FloatField()
    b=models.FloatField()