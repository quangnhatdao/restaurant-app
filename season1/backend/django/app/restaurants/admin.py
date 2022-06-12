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
    readonly_fields=('owner',)
    fieldsets = [
        (None,               {'fields': ['name']}),
        (None,               {'fields': ['address']}),
        (None,               {'fields': ['tags']}),
        (None,               {'fields': ['image']})
    ]
    inlines = [DishInline]
    list_display = ('name', 'address', 'owner')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.owner != request.user:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.owner != request.user:
            return False
        return True

admin.site.register(Restaurant, RestaurantAdmin)