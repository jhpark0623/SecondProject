from django.contrib import admin

from second.models import ParkingBasic, ParkingAvailability, Camera, Favorite

# Register your models here.
admin.site.register(ParkingBasic)
admin.site.register(ParkingAvailability)
admin.site.register(Camera)
admin.site.register(Favorite)