from django.shortcuts import render,redirect,get_object_or_404
from adminpage.forms import (loginForm,registerForm,
                            roomBuildingForm,ProfileForm,ProfilePic,
                            resetPasswordForm)
from django.contrib import messages
import time
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from adminpage.models import RoomServer,userProfile,TemperatureStore,TemperatureRoom
from django.contrib.auth import logout,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group,User
from adminpage.decoration import authenticate,unanthenticated_user,allow_subadmins,admin_only
import json
from django.views.generic import View
from django.db.models import Avg
import datetime
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger


# Create your views here.
@unanthenticated_user
def adminLogin(request):
    form = loginForm(request.POST or None)
    if request.method =="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            return redirect('adminpage')
        else:
            messages.error(request,'Account not exists or wrong username or password')
    return render(request,'adminauth/login.html',{'form':form,'message':messages})


#admin page
@login_required(login_url='adminLogin')
@admin_only
def adminpage(request):
    user = User.objects.all()
    context={
        'user':user,
    }
    return render(request,'adminall/adminpage.html',context)

#go check subadmin
@login_required(login_url='adminLogin')
@admin_only
def checkSubadminPage(request,user):
    room=RoomServer.objects.filter(user__username=user)
    return render(request,'adminall/subAdmin.html',{'room':room,'username':user})


#logout link
@login_required(login_url='adminLogin')
def logoutpage(request):
    logout(request)
    return redirect('adminpage')

#register 
@allow_subadmins(allowed_roles=['admin'])
@login_required(login_url='adminLogin')
def register(request):
    form = registerForm(request.POST or None)
    
    if request.method == "POST":
        form = registerForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password2')
            current_site = get_current_site(request)
            print(username)
            group = Group.objects.get(name = "subadmin")
            user.groups.add(group)
            pObj =User.objects.get(username=username)
            userProfile(user = pObj,phone="none").save()
            mail_subject = "Activate your account as subadmin"
            message = render_to_string('email/emailverify.html',{
                'user':user,
                'domain':current_site,
                'email':email,
                'password':password,
            })
            email = EmailMessage(mail_subject,message,to=[email])
            email.send()
            messages.success(request,'Account has been created')
        print(form.errors)
        return redirect('register')
    return render(request,'adminall/register2.html',{'form':form,'message':messages})

#profile page
@allow_subadmins(allowed_roles=['subadmin'])
def profile(request):
    user = request.user
    profile=request.user.userprofile
    forms = ProfilePic(instance=profile)
    form = ProfileForm(instance=user)
    if request.method == "POST":
        form= ProfileForm(request.POST,instance=user)
        forms = ProfilePic(request.POST,request.FILES,instance=profile)
        print(forms)
        if form.is_valid():
            form.save()
        if forms.is_valid():
            forms.save()
    content={'user':user,'form':form,'forms':forms}
    return render (request,'admin/profile.html',content)
#password modal
def passwordView(request):
    data= dict()
    user= request.user
    form_reset=resetPasswordForm(data=request.POST,user=user)
    print(form_reset)
    if form_reset.is_valid():
        form_reset.save()
        data['form_is_valid']=True
    else:
        data['form_is_valid']=False
    data['html_list'] = render_to_string("admin/profilemodel.html",{'form_reset':form_reset},request=request)
  
    return JsonResponse(data)

#subadmin
#page user
@login_required(login_url="adminLogin")
@allow_subadmins(allowed_roles=['subadmin'])
def subadmin(request):
    subadmins = request.user 
    user = User.objects.get(username=subadmins)
    print(user)
    form = roomBuildingForm(request.POST or None)
    reponse=dict()
    room = RoomServer.objects.filter(user =subadmins)
    if request.method == "POST":
        form = roomBuildingForm(request.POST or None)
        if form.is_valid():
            roombuilding = form.cleaned_data['buildingRoom']
            print(type(roombuilding))
            p=RoomServer(user=user,buildingRoom=roombuilding)
            p.save()
            response={
            'room':roomBuilding,
            }
    context={
        'user':subadmins,
        'room':room,
        'form':form
        }
    print(context)
    print(subadmin)
    return render(request,'subadmin/subadmin.html',context)

def save_update_room_subuser(request,form,template_name):
    data = dict()
    user =request.user
    print(user)
    if request.method =="POST":
        if form.is_valid():
            p=form.cleaned_data.get("buildingRoom")
            form.buildingRoom=p
            print(form.buildingRoom)
            form.save()
            room=RoomServer.objects.filter(user__username=user)
            data['form_is_valid']=True
            data['html_room_list'] =render_to_string('subadmin/roomlist/listroom.html',{'room':room})
        else:
            data['form_is_valid']= False
    context={'form':form}
    print(context)
    data['html_room_form']= render_to_string(template_name, context, request=request)
    print(data)
    return JsonResponse(data)

#reload data in room and save data to room
def save_room_subuser(request,form,template_name):
    data = dict()
    user =request.user 
    print(user)
    if request.method =="POST":
        if form.is_valid():
            save_method = form.save(commit=False)
            save_method.user = user
            save_method.save()
            room=RoomServer.objects.filter(user__username=user)
            data['form_is_valid']=True
            data['html_room_list'] =render_to_string('subadmin/roomlist/listroom.html',{'room':room})
        else:
            data['form_is_valid']= False
    context={'form':form}
    print(context)
    data['html_room_form']= render_to_string(template_name, context, request=request)
    print(data)
    return JsonResponse(data)

#add room at sub admin page
def create_roomSub(request):
    form = roomBuildingForm()
    print(form)
    if request.method == "POST":
        form = roomBuildingForm(request.POST)
    return save_room_subuser(request , form,'subadmin/roomlist/createroom.html')

#update at subadmin
def update_roomSub(request,roomBuilding):
    user = request.user
    data=dict()
    room = RoomServer.objects.filter(buildingRoom=roomBuilding)
    if room.exists():
        room = RoomServer.objects.get(buildingRoom=roomBuilding)
        form = roomBuildingForm(instance=room)
        if request.method == "POST":
            form = roomBuildingForm(request.POST,instance=room)
    return save_update_room_subuser(request,form,'subadmin/roomlist/updateroom.html')

#delete at subadmin
def roomSub_delete(request,roomBuilding):
    data=dict()
    user = request.user
    room = RoomServer.objects.filter(buildingRoom=roomBuilding)
    if room.exists():
        room = RoomServer.objects.get(buildingRoom=roomBuilding)
        if request.method == "POST":
            room.delete()
            data['form_is_valid'] = True
            rooms = RoomServer.objects.filter(user= user)
            data['html_room_list'] = render_to_string('subadmin/roomlist/listroom.html',{'room':rooms})
        else:
            context = {'room':room}
            
            data['html_room_form'] = render_to_string('subadmin/roomlist/deleteroom.html',context,request=request)
    return JsonResponse(data)

#temperature for sub admin
def getTemperatureSub(request,roomBuilding):
    data=dict()
    temp=list()
    time=list()
    room=""
    graph = str(roomBuilding)
    user = TemperatureRoom.objects.filter(room__buildingRoom = graph).order_by("-date_and_time")[:10]
    if user.exists():
        for data in user:
            temper = float("%.2f"%(data.Temperature))
            room= data.room
            temp.append(temper)
            time.append(data.date_and_time.time())
        print(temp.reverse())
        data={
            'room':str(room.buildingRoom),
            'temperature':temp,
            'date_and_time':time,
        }
        return JsonResponse(data)
    return JsonResponse(data)

#send mail alert
def sendMail(request):
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
                current_site = get_current_site(request)
                mail_subject = "Warning The temperature is Too High" 
                user = TemperatureRoom.objects.filter(room__buildingRoom=data.room.buildingRoom)[0].room.user
                message = render_to_string('email/sendtemperature.html',{
                    'user':user,
                    'room': data.room.buildingRoom,
                    'temperature': data.Temperature,
                    'domain':current_site,
                })
                email = TemperatureRoom.objects.filter(room__buildingRoom=data.room.buildingRoom)[0].room.user.email
                email = EmailMessage(mail_subject,message,to=[email])
                email.send()
            # return JsonResponse(dat)
        dat={
            'data':dataload,
        }
    return JsonResponse(dat)

#reset the data for an hour and put it back
def resetdataHour(request):
    dat = dict()
    room = RoomServer.objects.all()
    if room.exists():
        for data in room:
            allTemperatureInRoom=TemperatureRoom.objects.filter(room=data.pk)
            if allTemperatureInRoom.exists():
                averagePerHour =allTemperatureInRoom.aggregate(Avg('Temperature')).get("Temperature__avg")
                allTemperatureInRoom.delete()
                count= allTemperatureInRoom.count()
                print(count)
                print(allTemperatureInRoom)
                print(type(averagePerHour))
                p=TemperatureRoom(room=RoomServer.objects.get(pk=data.pk),Temperature="%.2f"%(averagePerHour),date_and_time=datetime.datetime.now())
                p.save()
    return JsonResponse(dat)

#reset per day put in temperature store
def resetperDay(request):
    dat=dict()
    print(datetime.datetime.now().date())
    room = RoomServer.objects.all()
    if room.exists():
        for data in room:
            allTemperatureInRoom=TemperatureRoom.objects.filter(room=data.pk)
            if allTemperatureInRoom.exists():
                averagePerHour =allTemperatureInRoom.aggregate(Avg('Temperature')).get("Temperature__avg")
                allTemperatureInRoom.delete()
                count= allTemperatureInRoom.count()
                print(count)
                print(allTemperatureInRoom)
                print(type(averagePerHour))
                p=TemperatureStore(room=RoomServer.objects.get(pk=data.pk),Temperature="%.2f"%(averagePerHour),date=datetime.datetime.now().date())
                p.save()
    return JsonResponse(dat)

#History
def historysub(request):
    user = request.user
    temperature = TemperatureStore.objects.filter(room__user__username=user)
    page = request.GET.get('page',1)
    paginator = Paginator(temperature,8)
    print(temperature)
    
    try:
        room = paginator.page(page)
    except PageNotAnInteger:
        room = paginator.page(1)
    except EmptyPage:
        room = paginator.page(paginator.num_pages)
    return render(request,'subadmin/history/history.html',{'room':room})
 
#search function history
def searchhistorysub(request):
    data = dict()
    roomid = request.GET.get("page")
    temperature=TemperatureStore.objects.filter(room__buildingRoom=roomid)
    print(temperature)
    paginator = Paginator(temperature,8)
    data['form.is_valid']=True
    page = request.GET.get('page',1)
    try:
        room = paginator.page(page)
    except PageNotAnInteger:
        room = paginator.page(1)
    except EmptyPage:
        room = paginator.page(paginator.num_pages)
    data['html_list'] = render_to_string("subadmin/history/historylist.html",{'room':room},request=request)
    data['html_list_pagination'] = render_to_string("subadmin/history/paginationhistory.html",{'room':room},request=request)
    return JsonResponse(data)

#search data as date
def searchdatesub(request):
    data = dict()
    dat= list()
    room=None
    user=request.user
    roomid = request.GET.get("date_and_day")
    roomid = datetime.datetime.strptime(roomid,'%Y-%m-%d').date()
    temperature = TemperatureStore.objects.filter(room__user__username=user)
    if temperature.exists():
        for i in temperature:
            if roomid==i.date:
                dat.append(i)
    paginator = Paginator(dat,8)
    print(paginator)
    page = request.GET.get('page',1)
    try:
        room = paginator.page(page)
    except PageNotAnInteger:
        room = paginator.page(1)
    except EmptyPage:
        room = paginator.page(paginator.num_pages)
    data['html_list']=render_to_string("subadmin/history/historylist.html",{'room':room},request=request)
    data['html_list_pagination'] = render_to_string("subadmin/history/paginationhistory.html",{'room':room},request=request)
    return JsonResponse(data)