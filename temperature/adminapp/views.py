from django.shortcuts import render

# Create your views here.
def loginAdmin(request):
    return render(request,"adminauth/login.html")
    