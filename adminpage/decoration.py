from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect
from adminpage.models import userProfile
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

#not allow admin return some page

def unanthenticated_user(view_func):
    def wrapper_func(request,*args, **kwargs):
        if request.user.is_authenticated:
            redirect('adminpage')
        return view_func(request,*args, **kwargs)
    return wrapper_func
# # example restrict the page
def allow_subadmins(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request,*args, **kwargs):
            group = None    #if group none
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request,*args, **kwargs)
            else:
                return HttpResponse("Hey man")
        return wrapper_func
    return decorator

# #allow json to get the data
    
#use in view to restrict on sidebar
def admin_only(view_func):
    def wrapper_func(request,*args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == "subadmin":
            return redirect('subadmin')
        elif group == "admin":
            return view_func(request,*args, **kwargs)
    return wrapper_func

def authenticate(request,email,password):
    """
    Check authenticate on email and password
    """
    user = User.objects.filter(email=email)
    if user.exists():
        user = User.objects.get(email=email)
        if user.check_password(password):
            return user
    return None
