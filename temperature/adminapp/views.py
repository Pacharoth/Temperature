from django.shortcuts import render
from adminapp.forms import loginForm

# Create your views here.
def loginAdmin(request):
    form = loginForm(request.POST or None)
    
    return render(request,"adminauth/login.html")
    