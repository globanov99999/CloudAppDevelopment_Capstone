from django.contrib import admin

from .models import CarMake
from .models import CarModel


class CarModelInline(admin.TabularInline):
    model = CarModel

class CarModelAdmin(admin.ModelAdmin):
   inlines = [CarModelInline]

class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]

admin.site.register(CarMake,CarMakeAdmin)
admin.site.register(CarModel)

