from django.db import models
from django.contrib.auth.models import User

"""
model for restaurant
"""
class Restaurant(models.Model):
    owner = models.ForeignKey(User, editable=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    tags = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/restaurants/')

    def __str__(self):
        return self.name

"""
model for dish
"""
class Dish(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/dishes/')

    def __str__(self):
        return self.name
