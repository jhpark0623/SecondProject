from django.contrib import admin

from second.models import ParkingBasic, ParkingAvailability

# Register your models here.
admin.site.register(ParkingBasic)
admin.site.register(ParkingAvailability)