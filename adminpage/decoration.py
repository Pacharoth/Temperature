from django.http import HttpResponse
from django.shortcuts import redirect

#not allow admin return some page
def unauthicated_user(view_func):
    def wrap_func(request,*args, **kwargs):
        if request.user.is_authenticated:
            return redirect('adminpage')
        else:
            return view_func(request,*args, **kwargs)
    return wrap_func

# example restrict the page
def allow_subadmins(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request,*args, **kwargs):
            
            group = None    #if group none
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request,*args, **kwargs)
            else:
                return HttpResponse('You are suck')
        return wrapper_func
    return decorator

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