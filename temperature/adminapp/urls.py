from django.urls import path
from adminapp import views
app_name = "admin_page"
urlpatterns = [
    path("login/", views.loginAdmin,name="adminlogin"),
    
]
