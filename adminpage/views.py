from django.shortcuts import render,redirect
from adminpage.forms import (loginForm,registerForm,
                            roomBuilding,ProfileForm,ProfilePic)
from django.contrib import messages
from django.http import JsonResponse

from adminpage.models import RoomServer
from django.contrib.auth import logout,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group,User
from adminpage.decoration import authenticate,unanthenticated_user,allow_subadmins
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

# def userCard(request):
#     return render()
#admin page
@login_required(login_url='adminLogin')
def adminpage(request):
    return render(request,'admin/admin.html')

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
    room = roomBuilding(request.POST or None)
    if request.method == "POST":
        if form.is_valid() and room.is_valid():
            user = form.save()
            subadmin = room.save()
            user.subadmin.add()
            group = Group.objects.get(name = "subadmin")
            user.group.add()
        return redirect('adminLogin')
    return render(request,'adminauth/register.html',{'form':form,'room':room})

#profile page
@allow_subadmins(allowed_roles=['admin'])
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


#render the room in to json
def addRoom(request):
    user = request.user.profileuser
    data={}
    data_user=[]
    if request.method == "POST":
        roomid = request.POST.get("room")
        room = RoomServer.objects.all()
        if room.exists():
            room = RoomServer.objects.filter(user__name=user,buildingRoom=roomid)
        
    return JsonResponse(room)


#page user

def subadmin(request):
    subadmins = request.user
    # user =request.user
    room = RoomServer.objects.all()
    if request.method == "POST":
        roomData = request.POST.get('roomData')
        data=RoomServer(user=subadmin,buildingRoom=roomData)
        roomDat = data.save()
        return JsonResponse(data)
    if room.exists():
        room = RoomServer.objects.filter(user__name=subadmins)
        print(room)         
    context={'user':subadmins,'room':room}
    print(subadmin)
    return render(request,'subadmin/subadmin.html',context)

#reload data in room

def reloadRoom(request):
    subadmins = request.user.profileuser
    print(subadmins)
    room = RoomServer.objects.all()
    # data = {}
    dataToAppend=[]
    if room.exists():
        room = RoomServer.objects.filter(user__name = subadmins)
        for i in room:
            dataToAppend.append(str(i))
    data={
        'room':dataToAppend,
    }
    return JsonResponse(data)

