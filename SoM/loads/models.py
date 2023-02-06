from django.db import models

# Create your models here.
class ForceModel(models.Model):
    x=models.TextField()
    y=models.TextField()
    x1=models.FloatField()
    x2=models.FloatField()
    
    
class MomentModel(models.Model):
    x=models.TextField()
    z=models.TextField()
    x1=models.FloatField()
    x2=models.FloatField()
