# from django.db import models
from djongo import models

# Create your models here.

#register user
class userAccount(models.Model):
    username = models.CharField(max_length=100,primary_key=True)
    email = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=100)
    def __str__(self):
        return self.username
    