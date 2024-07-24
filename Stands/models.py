from django.db import models

# Create your models here.

class Area(models.Model):
    a_no=models.PositiveIntegerField(unique=True)
    a_name=models.CharField(max_length=100)
    
    class Meta:
        ordering=['a_name']
    
    def __str__(self):
        return self.a_name


class Stand(models.Model):
    s_no=models.PositiveIntegerField(unique=True)
    s_name=models.CharField(max_length=100)
    lati = models.FloatField(blank=True,null=True)
    longi = models.FloatField(blank=True,null=True)
    trafficCof=models.PositiveIntegerField(default=50)
    area=models.ManyToManyField(Area)
    
    class Meta:
        ordering=['s_name']
    
    def __str__(self):
        return self.s_name