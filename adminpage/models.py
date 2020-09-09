# from django.db import models
from djongo import models
from django.contrib.auth.models import User
import os

# Create your models here.

#Profile user
# class ProfileUser(models.Model):
#     user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
#     name = models.CharField(max_length=200,null = True)
#     phone = models.CharField(max_length=200,null=True,blank=True)
#     email= models.EmailField(max_length=100,null=True,blank=True)
#     img  = models.ImageField(upload_to='imgprofile/',null = True,blank=True)
#     def __str__(self):
#         return self.name

#user
class userProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=100,unique=True)
    img = models.ImageField(upload_to='imgprofile/')
    def __str__(self):
        return self.phone
    
    
#Room 
class RoomServer(models.Model):
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    buildingRoom = models.CharField(max_length=100,primary_key=True)
    def __str__(self):
        return self.buildingRoom

#change password form in user


#store temperature in room
class TemperatureRoom(models.Model):
    room = models.ForeignKey(RoomServer,null=True,on_delete=models.CASCADE)
    Temperature = models.FloatField()
    date_and_time = models.DateTimeField()
    

class TemperatureStore(models.Model):
    room = models.ForeignKey(RoomServer,null=True,on_delete=models.CASCADE)
    Temperature = models.FloatField()
    date = models.DateField()
    

    