from django.urls import path,re_path
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
    re_path(r'^subadmin/(?P<roomBuilding>\w+)/request/$',views.getTemperatureSub, name="tempSub"),
    path('adminpage/subadmin',views.checkSubadminPage,name="checksub"),
    re_path(r'^subadmin/(?P<roomBuilding>\w+)/update/$',views.update_roomSub,name="updateroomsub"),
    re_path(r'^subadmin/(?P<roomBuilding>\w+)/delete/$',views.roomSub_delete,name="deleteroomsub"),
    re_path(r'^subadmin/create/$',views.create_roomSub,name="createroomsub"),
    path('sendmail/',views.sendMail,name="sendmail")
]
