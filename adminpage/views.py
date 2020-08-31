from django.shortcuts import render,redirect
from adminpage.forms import loginForm
from django.contrib import messages
from django.contrib.auth import login,authenticate
# Create your views here.

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

def adminpage(request):
    return render(request,'admin/admin.html')