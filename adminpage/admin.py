from django.contrib import admin
from adminpage import models
admin.site.register(models.userProfile)
admin.site.register(models.RoomServer)
admin.site.register(models.TemperatureRoom)
admin.site.register(models.TemperatureStore)
