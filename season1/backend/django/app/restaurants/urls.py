from django.urls import path

from . import views

"""
urls
"""
urlpatterns = [
    path('restaurants/', views.restaurant_list, name='restaurant_list'),
    path('restaurants/<int:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),
    path('restaurants/<int:restaurant_id>/upload_image/', views.restaurant_upload_image, name='restaurant_upload_image'),
    path('restaurants/<int:restaurant_id>/dishes/', views.dish_list, name='dish_list'),
    path('restaurants/<int:restaurant_id>/dishes/<int:dish_id>/', views.dish_detail, name='dish_detail'),
    path('restaurants/<int:restaurant_id>/dishes/<int:dish_id>/upload_image/', views.dish_upload_image, name='dish_upload_image')
]