from django.shortcuts import render,redirect
from adminpage.forms import (loginForm,registerForm,
                            roomBuilding,ProfileForm,ProfilePic,resetPasswordForm)
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from adminpage.models import RoomServer,userProfile
from django.contrib.auth import logout,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group,User
from adminpage.decoration import authenticate,unanthenticated_user,allow_subadmins,admin_only
from adminpage.utils import render_to_pdf
from django.views.generic import View
import secrets
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
@admin_only
def adminpage(request):
    return render(request,'alladmin/adminpage.html')

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
            message = render_to_string('emailverify.html',{
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


#render the room in to json
@allow_subadmins(allowed_roles=['subadmin'])
@login_required(login_url="adminLogin")
def addRoom(request):
    user = request.user
    subadmin = User.objects.get(username=user)
    data={}
    data_user=[]
    if request.method == "POST":
        roomid = request.POST.get("buidlingRoom")
        user = RoomServer(user=subadmin,buildingRoom=roomid).save()
    return JsonResponse(room)

#delete room
def deleteRoom(request):
    data=[]
    if request.method == "POST":
        roomid = request.POST.get("roomDelete")
        room = RoomServer.objects.filter(buildingRoom=roomid)
        if room.exists():
            room.delete()
    return JsonResponse(data)


#page user
@login_required(login_url="adminLogin")
@allow_subadmins(allowed_roles=['subadmin'])
def subadmin(request):
    subadmins = request.user 
    user = User.objects.get(username=subadmins)
    print(user)
    form = roomBuilding(request.POST or None)
    reponse={}
    room = RoomServer.objects.filter(user =subadmins)
    if request.method == "POST":
        form = roomBuilding(request.POST or None)
        
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
    print(subadmin)
    return render(request,'subadmin/subadmin.html',context)


#reload data in room
def reloadRoom(request):
    subadmins = request.user
    print(subadmins)
    room = RoomServer.objects.all()
    # data = {}
    dataToAppend=[]
    if room.exists():
        room = RoomServer.objects.filter(user__username = subadmins)
        for i in room:
            dataToAppend.append(str(i))
        data={
            'roomsubadmin':dataToAppend,
        }
    return JsonResponse(data)

#send 