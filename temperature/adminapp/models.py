# from django.db import models
from djongo import models
# Create your models here.


#Admin models
class adminControl(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)\
    
    def __str__(self):
        return self.last_name

    
    
