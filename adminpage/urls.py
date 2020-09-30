from django.urls import path,re_path
from adminpage import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User 
from adminpage.views_admin import (generateWeeklyForm,
                                generateMonthlyForm,
                                generateAnnuallyForm,renderAnnuallyReport,
                                renderWeeklyReport,renderMonthlyReport)
from adminpage import views_admin
urlpatterns = [

    #Authenticate Subadmin and Admin
    path('',views.adminLogin,name ="adminLogin"),
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
    re_path(r"^api/year/$",views_admin.avgApiYear,name="apiyear"),
    path('adminpage/',views.adminpage,name = "adminpage"),
    path('adminpage/register/',views.register,name = 'register'),
    re_path(r'^adminpage/subadmin/(?P<user>\w+)/',views.checkSubadminPage,name="checksub"),
    path('temperature/api/',views_admin.getTemperatureAdmin,name="temperatureadmin"),
    path('sendmail/',views.sendMail,name="sendmail"),
    path("adminpage/history/",views_admin.historyAdmin,name="historyadmin"),
    path("adminpage/profile/",views_admin.adminProfile,name="adminprofile"),
    re_path(r"^room/createroom/$",views_admin.create_roomAdmin,name="createroomadmin"),
    re_path(r"^room/update/$",views_admin.update_roomAdmin,name="updateroomadmin"),
    re_path(r"^room/delete/$",views_admin.delete_roomAdmin,name="deleteroomadmin"), 
    # path("profileAdmin/",views_admin.adminApi,name="userform"),
    path("adminpage/api/",views_admin.passwordAdmin,name="passwordadmin"),
    path("adminpage/search/",views_admin.searchdateadmin,name="searchhistory"),
    path("adminpage/user/",views_admin.userpage,name="userpage"),
    path("adminpage/user/<int:pk>/edit/",views_admin.editUser,name="useredit"),
    path("adminpage/user/delete/",views_admin.deleteUser,name="userdelete"),
    path("adminpage/searchuser/user/",views_admin.searchUser,name="searchUser"),
]
