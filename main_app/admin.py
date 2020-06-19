from django.contrib import admin
from .models import Bird, Sighting, Location, BirdPhoto, LocationPhoto

# Register your models here.
admin.site.register(Bird)
admin.site.register(Sighting)
admin.site.register(Location)
admin.site.register(BirdPhoto)
admin.site.register(LocationPhoto)
