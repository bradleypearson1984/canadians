from django.db import models
from django.urls import reverse 
# Create your models here.


class Canadian(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=0)
    hometown = models.CharField(max_length=100)
    about = models.TextField(max_length=250)
    quote = models.TextField(max_length=250)
    
    def get_absolute_url(self):
        return reverse('canadians_detail', kwargs={'cat_id': self.id})
    
    def __str__(self):
        return self.name 
    

class Snack(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100) 

class City(models.Model):
    name = models.CharField(max_length=100)
    province = models.CharField(max_length=50)
    