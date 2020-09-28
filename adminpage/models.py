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
    phone = models.CharField(max_length=100,unique=True,blank=True,null=True)
    img = models.ImageField(upload_to='imgprofile/',blank=True,null=True)
    def __str__(self):
        return self.user.username
    
    def delete(self,*args, **kwargs):
        if os.path.isfile(self.img.path):
            os.remove(self.img.path)
        super(userProfile,self).delete(*args, **kwargs)
    
#Room 
class RoomServer(models.Model):
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    buildingRoom = models.CharField(max_length=100,unique=True)



#store temperature in room
class TemperatureRoom(models.Model):
    room = models.ForeignKey(RoomServer,null=True,on_delete=models.CASCADE)
    Temperature = models.FloatField()
    date_and_time = models.DateTimeField()


class TemperatureStore(models.Model):
    room = models.ForeignKey(RoomServer,null=True,on_delete=models.CASCADE)
    Temperature = models.FloatField()
    date = models.DateField()
    

    