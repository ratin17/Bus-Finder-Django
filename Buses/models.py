from django.db import models
from Stands.models import Stand
# Create your models here.

class Bus(models.Model):
    b_no=models.PositiveIntegerField(unique=True)
    b_name=models.CharField(max_length=100)
    stands=models.ManyToManyField(Stand,through="OrderingModel")
    rating=models.PositiveIntegerField(default=50)
    isActive=models.BooleanField(default=True)
    service=models.CharField(max_length=100,default="Semi-Sitting")
    
    class Meta:
        ordering=['-rating']
    
    def __str__(self):
        return self.b_name


class OrderingModel(models.Model):
    stand = models.ForeignKey(Stand, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(blank=True,null=True)

    class Meta:
        ordering=['-bus','order']
        
    def __str__(self):
        return self.bus.b_name+'-'+f'{self.order}-'+self.stand.s_name