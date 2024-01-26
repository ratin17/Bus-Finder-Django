from django.db import models

# Create your models here.

class Area(models.Model):
    a_name=models.CharField(max_length=50)
    
    class Meta:
        ordering=['a_name']
    
    def __str__(self):
        return self.a_name



class Stand(models.Model):
    s_name=models.CharField(max_length=50)
    lati = models.FloatField(blank=True,null=True)
    longi = models.FloatField(blank=True,null=True)
    area=models.ForeignKey(Area,on_delete=models.CASCADE,blank=True,null=True)
    
    class Meta:
        ordering=['s_name']
    
    def __str__(self):
        return self.s_name