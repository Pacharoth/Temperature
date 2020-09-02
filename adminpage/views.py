from django.shortcuts import render,redirect
from adminpage.forms import loginForm
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required

from adminpage.decoration import unauthicated_user
from adminpage.utils import render_to_pdf
from django.views.generic import View
# Create your views here.

@unauthicated_user
def adminLogin(request):
    form = loginForm(request.POST or None)
    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('adminpage')
        else:
            messages.error(request,'Account not exists or wrong username or password')
    return render(request,'adminauth/login.html',{'form':form,'message':messages})

#admin page
@login_required(login_url='adminLogin')
def adminpage(request):
    return render(request,'admin/admin.html')

#logout link
def logoutpage(request):
    logout(request)
    return redirect('adminpage')




#generate weekly
class GeneratePDF_weekly(View):
    def get(self,request,*args,**kwargs):
        data={}
       
        template = get_template("adminpage/reportpage.html")
        user = User.objects.get(username=request.user)
        count=roomRegister.objects.all().count()
        
        if count > 0:
            room_ID_to_check= request.GET['room_id']
            week_to_check = request.GET['week_form']
            month_to_check = request.GET['month_form']
            year_to_check = request.GET['year_form']
            username = roomRegister.user_of_room(room_ID_to_check)
            date=datetime.datetime.now().date
            week_data =check_all_data_week(room_ID_to_check,int(year_to_check),int(month_to_check),int(week_to_check))
            print(week_data)
            data ={
                'date':date,
                'user':user,
                'username':username,
                'weekday':week_data.get('objects'),
                'roomID':room_ID_to_check,
                'getavg':week_data.get('avgtotal')
                }
        pdf = render_to_pdf('adminpage/reportpage.html',data)
        if pdf:
            response = HttpResponse(pdf,content_type = 'application/pdf')
            filename = "Report_%s.pdf"%("weekly")
            content = "inline; filename=%s"%(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename=%s"%(filename)
            response['Content-Disposition']=content
            return response
        return HttpResponse("Not found")