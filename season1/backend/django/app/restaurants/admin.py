from django.contrib import admin

from .models import Restaurant, Dish

"""
inline entry for dish
"""
class DishInline(admin.TabularInline):
    model = Dish
    extra = 3

"""
admin page for restaurant
"""
class RestaurantAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
        (None,               {'fields': ['address']}),
        (None,               {'fields': ['tags']}),
        (None,               {'fields': ['image']})
    ]
    inlines = [DishInline]
    list_display = ('name', 'address')

admin.site.register(Restaurant, RestaurantAdmin)