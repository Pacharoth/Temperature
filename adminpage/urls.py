from django.urls import path,re_path
from adminpage import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User 
from adminpage.views_admin import (generateWeeklyForm,
                                generateMonthlyForm,
                                generateAnnuallyForm,renderAnnuallyReport,
                                renderWeeklyReport,renderMonthlyReport)
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
    re_path(r'^resetperhour/$',views.resetdataHour,name="resetperhoursub"),
    re_path(r'^resetperday/$',views.resetperDay,name="resetperdaysub"),
    path('subadmin/profile/',views.profile,name='profile'),
    path('subadmin/history/',views.historysub,name="historysub"),
    path('subadmin/history/search/',views.searchhistorysub,name="searchhistorysub"),
    path('subadmin/profile/api/',views.passwordView,name ="passwordView"),
    path('subadmin/profile/searchdate/',views.searchdatesub,name="searchdatesub"),
    path('download/weekly/',generateWeeklyForm,name="generateweekly"),
    path('download/monthly/',generateMonthlyForm,name="generatemonthly"),
    path('download/annully/',generateAnnuallyForm,name="generateannually"),
    re_path(r'^download/weekly$',renderWeeklyReport,name="generatepdf"),
    re_path(r'^download/monthly$',renderMonthlyReport,name="generatepdfmonth"),
    re_path(r'^download/annually$',renderAnnuallyReport,name="generatepdfannual"),

    #Admin url
    path('adminpage/',views.adminpage,name = "adminpage"),
    path('adminpage/register/',views.register,name = 'register'),
    path('adminpage/subadmin/',views.checkSubadminPage,name="checksub"),
    path('sendmail/',views.sendMail,name="sendmail")
]
