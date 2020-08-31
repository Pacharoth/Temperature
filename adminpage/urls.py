from django.urls import path
from adminpage import views
urlpatterns = [
    path('login/',views.adminLogin,name ="adminLogin"),
    path('',views.adminpage,name = "adminpage"),
    path('logout/',views.logoutpage,name = "logoutpage"),
]
