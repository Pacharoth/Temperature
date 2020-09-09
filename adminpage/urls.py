from django.urls import path
from adminpage import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User 
urlpatterns = [
    path('login/',views.adminLogin,name ="adminLogin"),
    path('adminpage/',views.adminpage,name = "adminpage"),
    path('register',views.register,name = 'register'),
    path('logout/',views.logoutpage,name = "logoutpage"),
    path('subadmin/',views.subadmin,name = 'subadmin'),
    path('profile/',views.profile,name='profile'),
    path('api/room/',views.reloadRoom,name="loadRoom")
]
