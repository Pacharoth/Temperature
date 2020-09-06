from django.shortcuts import render,redirect
from adminpage.forms import loginForm,registerForm,roomBuilding
from django.contrib import messages


from adminpage.models import ProfileUser,RoomServer
from adminpage.forms import ProfilePicForm
from adminpage.models import RoomServer
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group,User
from adminpage.decoration import unauthicated_user,allow_subadmins,admin_only
from adminpage.utils import render_to_pdf
from django.views.generic import View

from django.http import JsonResponse
# Create your views here.

@unauthicated_user
def adminLogin(request):
    form = loginForm(request.POST or None)
    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
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
    return render(request,'admin/admin.html')

#logout link
def logoutpage(request):
    logout(request)
    return redirect('adminpage')

#register 
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
@login_required(login_url='adminLogin')
@allow_subadmins(allowed_roles=['subadmin','admin'])
def profile(request):
    user = request.user.profileuser
    form = ProfilePicForm(instance=user)
    if request.method == "POST":
        form = ProfilePicForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
    return render (request,'admin/profile.html',{'user':user,'form':form})

@login_required(login_url='adminLogin')
@allow_subadmins(allowed_roles=['subadmin'])
#render the room in to json
def addRoom(request):
    user = request.user.profileuser
    data={}
    if request.method == "POST":
        roomid = request.POST.get("room")
        room = RoomServer.objects.all()
        if room.exists():
            room = RoomServer.objects.filter(user__name=user,buildingRoom=roomid)
        data = {
            'obj':room,
        }
    return JsonResponse(data)


#page user
@allow_subadmins(allowed_roles=['subadmin'])
@login_required(login_url='adminLogin')
def subadmin(request):
    subadmins = request.user.profileuser
    room = RoomServer.objects.all()
    if room.exists():
        room = RoomServer.objects.filter(user__name=subadmins)
    context={'user':subadmins,'room':room}
    print(subadmin)
    return render(request,'subadmin/subadmin.html',context)

#generate weekly

