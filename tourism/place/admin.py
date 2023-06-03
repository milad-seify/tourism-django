from django.contrib.gis import admin
from . import models


@admin.register(models.Places)
class PlacesAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'type')


@admin.register(models.RecreationalPlace)
class RecAdmin(admin.OSMGeoAdmin):
    list_display = ('location', 'image')


@admin.register(models.ShoppingPlace)
class ShopAdmin(admin.OSMGeoAdmin):
    list_display = ('location', 'image')


@admin.register(models.TourismPlace)
class TourismAdmin(admin.OSMGeoAdmin):
    list_display = ('location', 'image')
