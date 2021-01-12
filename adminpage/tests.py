from django.test import TestCase
from adminpage.views import (
    User,userProfile,render_to_string,messages,
    render,Group,login_required,unanthenticated_user
    ,allow_subadmins,admin_only,Avg,JsonResponse
    ,Q,datetime)
from django.contrib.sites.shortcuts import get_current_site
from adminpage.models import TemperatureStore,RoomServer,userProfile,TemperatureRoom
import os
from adminpage.utils import monthList
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from temperature.settings import EMAIL_HOST_USER
from django.core.mail import EmailMessage
import time
from django.contrib.staticfiles import finders
from adminpage.forms import (choiceForm_weekly,choiceForm_annually,
                            choiceForm_monthly,resetPasswordForm,editGroupForm,phoneForm,editUserForm)
from adminpage.utils import weekList,monthList,annuallyList
from adminpage.forms import roomBuildingForm,ProfileForm,ProfilePic
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import httpx
import pytz
# Create your tests here.

def sendMail(data):
    dat=dict()
    count=0
    dataload=list()
    room = TemperatureRoom.objects.all().order_by('-date_and_time')[:15]
    if room.exists():
        for data in room:
            dataload.append(data.Temperature)
            if data.Temperature>=25:
                count+=1
            if count>=10:
                mail_subject = "Warning The temperature is Too High" 
                user = TemperatureRoom.objects.filter(room__buildingRoom=data.room.buildingRoom)[0].room.user
                message = render_to_string('email/sendtemperature.html',{
                    'user':user,
                    'room': data.room.buildingRoom,
                    'temperature': data.Temperature,
                    # 'domain':current_site,
                })
                time.sleep(1)
                email = TemperatureRoom.objects.filter(room__buildingRoom=data.room.buildingRoom)[0].room.user.email
                email = EmailMessage(mail_subject,message,EMAIL_HOST_USER,to=[email])
                email.send()
                print(email.send())
            # return JsonResponse(dat)
        dat={
            'data':dataload,
            'email':EMAIL_HOST_USER
            
        }
    return JsonResponse(dat)
sendMail(request="B220")