from django.urls import path,re_path
from adminpage import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User 
urlpatterns = [

    #Authenticate Subadmin and Admin
    path('login/',views.adminLogin,name ="adminLogin"),
    path('logout/',views.logoutpage,name = "logoutpage"),
    path('subadmin/',views.subadmin,name = 'subadmin'),

    #Subadmin url
    re_path(r'^subadmin/(?P<roomBuilding>\w+)/request/$',views.getTemperatureSub, name="tempsub"),
    re_path(r'^subadmin/(?P<roomBuilding>\w+)/update/$',views.update_roomSub,name="updateroomsub"),
    re_path(r'^subadmin/(?P<roomBuilding>\w+)/delete/$',views.roomSub_delete,name="deleteroomsub"),
    re_path(r'^subadmin/create/$',views.create_roomSub,name="createroomsub"),

    #Admin url
    path('adminpage/',views.adminpage,name = "adminpage"),
    path('subadmin/profile/',views.profile,name='profile'),
    path('adminpage/register/',views.register,name = 'register'),
    path('adminpage/subadmin',views.checkSubadminPage,name="checksub"),
    path('sendmail/',views.sendMail,name="sendmail")
]
