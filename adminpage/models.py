# from django.db import models
from djongo import models
from django.contrib.auth.models import User
# Create your models here.

#Profile user
class ProfileUser(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null = True)
    phone = models.CharField(max_length=200,null=True)
    email= models.CharField(max_length=100,null=True)
    img  = models.ImageField(null = True,blank=True)
    def __str__(self):
        return self.name
    
    

#Room 
class RoomServer(models.Model):
    user = models.ForeignKey(ProfileUser,null=True,on_delete=models.CASCADE)
    buildingRoom = models.CharField(max_length=100,primary_key=True)
    def __str__(self):
        return self.buildingRoom
    
    
#store temperature in room
class TemperatureRoom(models.Model):
    room = models.ForeignKey(RoomServer,null=True,on_delete=models.CASCADE)
    Temperature = models.FloatField()
    date_and_time = models.DateTimeField()
    

class TemperatureStore(models.Model):
    room = models.ForeignKey(RoomServer,null=True,on_delete=models.CASCADE)
    Temperature = models.FloatField()
    date = models.DateField()
    

    