from django import forms
from django.forms import ModelForm
from .models import Restaurant, Dish

"""
form for uploading image
"""
class UploadImageForm(forms.Form):
    image = forms.ImageField()

class RestaurantForm(ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'tags', 'image']

class DishForm(ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'description', 'price', 'restaurant', 'image']