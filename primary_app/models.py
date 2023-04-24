from django.db import models
from django.urls import reverse 
from django.contrib.auth.models import User

# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=100)
    province = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('city_detail', kwargs={'city_id': self.id})
    
    def __str__(self):
        return self.name 

class Canadian(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=0)
    hometown = models.CharField(max_length=100)
    about = models.TextField(max_length=250)
    quote = models.TextField(max_length=250)
    cities = models.ManyToManyField(City)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def get_absolute_url(self):
        return reverse('canadian_detail', kwargs={'canadian_id': self.id})
    
    def __str__(self):
        return self.name 
    

class Snack(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    


class Photo(models.Model):
    url = models.CharField(max_length=200)
    canadian = models.ForeignKey(Canadian, on_delete=models.CASCADE)

    def __str__(self):
        return f"photo for canadian_id: {self.canadian_id} @{self.url}"

