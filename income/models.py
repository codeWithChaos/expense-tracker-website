from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Income(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    source = models.CharField(max_length=255)
    
    
    def __str__(self):
        return f"{self.source} "
    
    class Meta:
        ordering = ['-date']  # Ordering by date in descending order
        
        
class Source(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
    
