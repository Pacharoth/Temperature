# from django.db import models
from djongo import models
from django.contrib.auth.models import User
import os
import datetime
from pytz import timezone
from django.utils.timezone import now

class userProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=100,blank=True,null=True)
    img = models.ImageField(upload_to='imgprofile/',blank=True,null=True)
    def __str__(self):
        return self.user.username    
#Room 
class RoomServer(models.Model):
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    buildingRoom = models.CharField(max_length=100,unique=True)



#store temperature in room
class TemperatureRoom(models.Model):
    room = models.ForeignKey(RoomServer,null=True,on_delete=models.CASCADE)
    Temperature = models.FloatField()
    date_and_time = models.DateTimeField(default=now())


class TemperatureStore(models.Model):
    room = models.ForeignKey(RoomServer,null=True,on_delete=models.CASCADE)
    Temperature = models.FloatField()
    date = models.DateField()
    

    