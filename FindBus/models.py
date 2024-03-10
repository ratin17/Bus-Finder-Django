
from django.db import models

# Create your models here.

class Suggestion(models.Model):
    
    CHOICES = (
        ('predefinned', 'Pre-definned'),
        ('custom', 'Custom'),
    )
    
    title=models.TextField()
    isRead=models.BooleanField(default=False)
    time=models.DateTimeField(auto_now=True)
    s_type=models.CharField(max_length=30, choices=CHOICES)
    name=models.CharField(max_length=50,null=True,blank=True)
    email=models.EmailField(null=True,blank=True)
    
    class Meta:
        ordering=['-time']
    
    def __str__(self):
        return self.title