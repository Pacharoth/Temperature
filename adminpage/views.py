from django.shortcuts import render,redirect,get_object_or_404
from adminpage.forms import (loginForm,registerForm,
                            roomBuildingForm,ProfileForm,ProfilePic,
                            resetPasswordForm)
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from adminpage.models import RoomServer,userProfile,TemperatureStore,TemperatureRoom
from django.contrib.auth import logout,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group,User
from adminpage.decoration import authenticate,unanthenticated_user,allow_subadmins,admin_only
from adminpage.utils import render_to_pdf
from django.views.generic import View
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
    return render(request,'alladmin/adminpage.html',context)

#go check subadmin
@login_required(login_url='adminLogin')
@admin_only
def checkSubadminPage(request):
    return render(request,'alladmin/sub-adminpage.html')


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
            email = form.cleaned_data.get('email')
           
            pObj =User.objects.get(username=user)
            pSave = userProfile(user = pObj).save()
            print(pSave)
            password = form.cleaned_data.get('password2')
            print(password)
            current_site = get_current_site(request)
            group = Group.objects.get(name = "subadmin")
            print(group)
            user.groups.add(group)
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
    return render(request,'alladmin/register2.html',{'form':form,'message':messages})

#change Form
def resetPassword(request):
    user = request.user
    form = resetPasswordForm(request.POST or None,user=user)
    print(form)
    if request.method == "POST":
        form=resetPasswordForm(request.POST or None ,user=user)
        if form.is_valid():
            form.save()
    return render(request,"")


#profile page
@allow_subadmins(allowed_roles=['subadmin'])
def profile(request):
    user = request.user 
    profile=request.user.userprofile
    forms = ProfilePic(instance=profile)
    form = ProfileForm(instance=user)
    if request.method == "POST":
        form = ProfileForm(request.POST,request.FILES,instance=user)
        forms = ProfilePic(request.POST,request.FILES,instance=profile)
        print(forms)
        if form.is_valid():
            form.save()
        if forms.is_valid():
            forms.save()
    return render (request,'admin/profile.html',{'user':user,'form':form,'forms':forms})


#subadmin
#page user
@login_required(login_url="adminLogin")
@allow_subadmins(allowed_roles=['subadmin'])
def subadmin(request):
    subadmins = request.user 
    user = User.objects.get(username=subadmins)
    print(user)
    form = roomBuildingForm(request.POST or None)
    reponse={}
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


#reload data in room and save data to room
def save_room_subuser(request,form,template_name):
    data = dict()
    user =request.user
    if request.method =="POST":
        if form.is_valid():
            form.save()
            room=RoomServer.objects.filter(user__username=user)
            data['form_is_valid']=True
            data['html_room_list'] =render_to_string('roomlist/modalRoom.html',{'room':room})
        else:
            data['form_is_valid']= False
        context={'form':form}
        data['html_room_form']= render_to_string(template_name, context, request=request)
    return JsonResponse(data)

#add room at sub admin page
def create_roomSub(request):
    form = roomBuildingForm()
    if request.method == "POST":
        form = roomBuildingForm(request.POST)
    return save_room_subuser(request,form,'/roomlist/modalRoom.html')

#update at subadmin
def update_roomSub(request,roomBuilding):
    room = RoomServer.objects.filter(buildingRoom=str(roomBuilding))
    if room.exists():
        room = RoomServer.objects.get(buildingRoom=roomBuilding)
        form = roomBuildingForm(instance=room)
        if request.method == "POST":
            form = roomBuildingForm(request.POST,instance=room)
        return save_room_subuser(request, form,'roomlist/roomupdate.html')

#delete at subadmin
def roomSub_delete(request,roomBuilding):
    data=dict()
    user = request.user
    room = RoomServer.objects.filter(buildingRoom=str(roomBuilding))
    if room.exists():
        room = RoomServer.objects.get(buildingRoom=roomBuilding)
        if request.method == "POST":
            room.delete()
            data['form_is_valid'] = True
            rooms = RoomServer.objects.filter(user= user)
            data['html_room_list'] = render_to_string('roomlist/modalRoom.html',{'room':room})
        else:
            context = {'room':room}
            data['html_room_form'] = render_to_string('roomlist/roomdelete.html',context,request=request)
        return JsonResponse(data)

#temperature for sub admin
def getTemperatureSub(request,roomBuilding):
    data=dict()
    temp=[]
    time=[]
    room=""
    graph = str(roomBuilding)
    print(roomBuilding)
    user = TemperatureRoom.objects.filter(room__buildingRoom = graph)
    print(user)
    if user.exists():
        for data in user:
            temper = float("%.2f"%(data.Temperature))
            print(temper)
            room= data.room
            temp.append(temper)
            time.append(data.date_and_time.time())
            print(room)
            print(temp)
            print(time)
        data={
            'room':str(room),
            'temperature':temp,
            'date_and_time':time,
        }
        print(data)    
        return JsonResponse(data)
    return JsonResponse(data)

#send mail alert
def sendMail(request):
    dat=dict()
    room = TemperatureRoom.objects.all()
    if room.exists():
        for data in room:
            if data.Temperature >21:
                print("Close Auto")
            elif data.Temperature < 20:
                mail_subject = "Warning The temperature is Too High" 
                user = TemperatureRoom.objects.filter(room__buildingRoom=data.room)[0].room.user
                message = render_to_string('email/sendtemperature.html',{
                    'user':user,
                    'room': data.room,
                    'temperature': data.Temperature,
                    'domain':current_site,
                })
                email = TemperatureRoom.objects.filter(room__buildingRoom=data.room)[0].room.user.email
                email = EmailMessage(mail_subject,message,to=[email])
                email.send()
                return JsonResponse(dat)
    return JsonResponse(dat)

#reset the data for an hour and put it back

