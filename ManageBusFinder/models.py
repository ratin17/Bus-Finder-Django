from django.db import models

class LogCount(models.Model):
    
    count = models.BigIntegerField(default=0)

    def __str__(self):
        return f"Request Count: {self.count}"





class Log(models.Model):
    
    CHOICES = (
        ('view', 'View'),
        ('suggest', 'Suggest'),
        ('search', 'Search'),
        ('try', 'Try'),
        ('submit', 'Submit'),
    )
    
    title=models.TextField()
    time=models.DateTimeField(auto_now=True)
    type=models.CharField(max_length=20, choices=CHOICES,blank=True,null=True)
    
    class Meta:
        ordering=['-time']
    
    def __str__(self):
        return self.title