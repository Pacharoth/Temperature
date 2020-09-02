from django.contrib import admin
from adminpage import models
admin.site.register(models.ProfileUser)
admin.site.register(models.RoomServer)
admin.site.register(models.TemperatureRoom)
admin.site.register(models.TemperatureStore)
