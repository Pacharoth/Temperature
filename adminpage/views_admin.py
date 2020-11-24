from adminpage.views import (
    User,userProfile,render_to_string,messages,
    render,Group,login_required,unanthenticated_user
    ,allow_subadmins,admin_only,Avg,JsonResponse
    ,Q,datetime)
from adminpage.models import TemperatureStore,RoomServer,userProfile,TemperatureRoom
import os
from adminpage.utils import monthList
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from adminpage.forms import (choiceForm_weekly,choiceForm_annually,
                            choiceForm_monthly,resetPasswordForm,editGroupForm,phoneForm,editUserForm)
from adminpage.utils import weekList,monthList,annuallyList
from adminpage.forms import roomBuildingForm,ProfileForm,ProfilePic
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from asgiref.sync import sync_to_async
import httpx
import pytz

def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    else:
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path

def generateWeeklyForm(request):
    data=dict()
    form = choiceForm_weekly(request.POST or None)
    data['html_list']=render_to_string("generatereport/weekform.html",{'form':form,},request=request)
    return JsonResponse(data)

def generateMonthlyForm(request):
    data=dict()
    room = request.GET.get("room")
    form = choiceForm_monthly(request.POST or None)
    if form.is_valid():
        data['form_is_valid']=True
        template_path="generatereport/pdfymonth.html"
        
    else:
        data['form_is_valid'] = False
    data['html_list']=render_to_string("generatereport/monthform.html",{'form':form},request=request)
    return JsonResponse(data)
def generateAnnuallyForm(request):
    data=dict()
    room = request.GET.get("room")
    form = choiceForm_annually(request.POST or None)
    if form.is_valid():
        data['form_is_valid'] =True
        template_path="generatereport/pdfyear.html"
    else:
        data['form_is_valid']=False
    data['html_list']=render_to_string("generatereport/yearform.html",{'form':form},request=request)
    return JsonResponse(data)

#pdf for all like month year and weekly
def renderWeeklyReport(request):
    post = request.POST.get
    room,week,month,year = post("room"),post("week_form"),post("month_form"),post("year_form")
    template_path="pdfweek.html"
    context=dict()
    data,avg = weekList(room,int(week),int(month),int(year))
    temperature =TemperatureStore.objects.filter(room__buildingRoom=room)
    if temperature.exists():
        temperature=temperature[0]
    context={
        "user":temperature,
        'data':data,
        'avg':"%.2f"%avg,
        'room':room,
        'date':datetime.datetime.now(),
    }
    response = HttpResponse(content_type = 'application/pdf')
    filename= "Report_room%s-(week%s)-%s-%s.pdf"%(room,week,month,year)
    response['Content-Disposition'] = 'attachment; filename=%s'%(filename)
    template = get_template(template_path)
    html = template.render(context)
    if room and week and month and year:
        pisaStatus =pisa.CreatePDF(
            html,dest=response,link_callback=link_callback)
        if pisaStatus.err:
            print("error")
    return response

#render pdf month
def renderMonthlyReport(request):
    post = request.POST.get
    room,month,year = post("room"),post("month_form"),post("year_form")
    temperature =TemperatureStore.objects.filter(room__buildingRoom=room)
    if temperature.exists():
        temperature=temperature[0]
    template_path="pdfmonth.html"
    context=dict()
    data,avgweek,summation= monthList(room,int(month),int(year))
    context={
        "user":temperature,
        'data':data,
        'avg': avgweek,
        'avgmonth':summation,
        'room':room,
        'date':datetime.datetime.now(),
        # 'lastdate':data[-1].date,
    }
    response = HttpResponse(content_type = 'application/pdf')
    filename= "Report_room%s-(month%s)-%s.pdf"%(room,month,year)
    response['Content-Disposition'] = 'attachment; filename=%s'%(filename)
    template = get_template(template_path)
    html = template.render(context)
    if room and month and year:
        pisaStatus =pisa.CreatePDF(
            html,dest=response,link_callback=link_callback)
        if pisaStatus.err:
            print("error")
    return response

#annually report 
def renderAnnuallyReport(request):
    post = request.POST.get
    room,year = post("room"),post("year_form")
    template_path="pdfyear.html"
    data,avgmonth,month,avgyear= annuallyList(room,year)
    temperature =TemperatureStore.objects.filter(room__buildingRoom=room)
    if temperature.exists():
        temperature=temperature[0]
    context=dict()
    context={
        'user':temperature,
        'data':data,
        'avgmonth':avgmonth,
        'month':month,
        'avg':avgyear,
        'room':room,
        'date':datetime.datetime.now(),
    }
    response = HttpResponse(content_type = 'application/pdf')
    filename= "Report_room%s-year%s.pdf"%(room,year)
    response['Content-Disposition'] = 'attachment; filename=%s'%(filename)
    template = get_template(template_path)
    html = template.render(context)
    if room and year:
        pisaStatus =pisa.CreatePDF(
            html,dest=response,link_callback=link_callback)
        if pisaStatus.err:
            print("error")
    return response

#history admin
def historyAdmin(request):
    temperature=TemperatureStore.objects.all().order_by('-date')
    page = request.GET.get('page',1)
    paginator = Paginator(temperature,6)
    try:
        room = paginator.page(page)
    except PageNotAnInteger:
        room = paginator.page(1)
    except EmptyPage:
        room = paginator.page(paginator.num_pages)
    return render(request,"adminall/history/history.html",{'room':room})


#average month
def avgApiYear(request):
    data = dict()
    room = request.GET.get("room")
    year = datetime.datetime.now().year
    monthly = datetime.datetime.now().month
    temperature =TemperatureStore.objects.filter(room__buildingRoom=str(room))
    if temperature.exists():
        data['empty']=False
        datavg,avgmonth,month,avgyear=annuallyList(room,year)
        dataavg,avgweek,summation= monthList(room,monthly,year)
        data={'datayear':avgyear,'datamonth':summation,'username':temperature[0].room.user.username}
    else:
        data['empty']=True
    return JsonResponse(data)

# @sync_to_async
def getTemperatureAdmin(request):
    data=dict()
    temp=list()
    time=list()
    roomBuilding= request.GET.get("room")
    graph = roomBuilding
    user = TemperatureRoom.objects.filter(room__buildingRoom = graph).order_by("-date_and_time")[:10]
    if user.exists():
        for data in user:
            temper = float("%.2f"%(data.Temperature))
            room= data.room
            temp.append(temper)
            time.append(data.date_and_time.time())
        data={
            'room':str(room.buildingRoom),
            'temperature':temp,
            'date_and_time':time,

        }
        return JsonResponse(data)
    return JsonResponse(data)
def save_update_Admin(request,pk,user,form,template_name):
    data = dict()
    if request.method =="POST":
        if form.is_valid():
            form.save()
            room=RoomServer.objects.filter(user__username=user)
            data['form_is_valid']=True
            data['html_room_list'] =render_to_string('adminall/room/roomAdminlist.html',{'room':room,'username':user})
        else:
            data['form_is_valid']= False
    context={'form':form,"user":user}
    data['html_room_form']= render_to_string(template_name, context, request=request)
    return JsonResponse(data)
#create room 
def save_room_Admin(request,user,form,template_name):
    data = dict()
    if request.method =="POST":
        user = request.POST.get("username")
        user=User.objects.get(username=user)
        if form.is_valid():
            save_method = form.save(commit=False)
            save_method.user = user
            save_method.save()
            room=RoomServer.objects.filter(user__username=user)
            data['form_is_valid']=True
            data['html_room_list'] =render_to_string('adminall/room/roomAdminlist.html',{'room':room,'username':user})
        else:
            data['form_is_valid']= False

    context={'form':form,'user':user}
    data['html_room_form']= render_to_string(template_name, context, request=request)
    return JsonResponse(data)

def create_roomAdmin(request):
    user = request.POST.get("username")
    form = roomBuildingForm(request.POST or None)
    return save_room_Admin(request,user,form,'adminall/room/createroom.html')
def update_roomAdmin(request):
    user =  request.GET.get("username")
    roomBuilding= request.GET.get("room")
    pk = request.GET.get("pk")
    room = RoomServer.objects.filter(buildingRoom=roomBuilding)
    if room.exists():
        room=RoomServer.objects.get(buildingRoom=roomBuilding)
        form = roomBuildingForm(instance=room)
    if request.method =="POST":
        user =  request.POST.get("username")
        pk = request.POST.get("pk")
        room = RoomServer.objects.get(pk=pk)
        form=roomBuildingForm(request.POST,instance=room)
    return save_update_Admin(request,pk,user,form,'adminall/room/updateroom.html')

#delete room
def delete_roomAdmin(request):
    data=dict()
    roombuilding= request.GET.get("room")
    user=request.GET.get("username")
    if request.method == "POST":
        user = request.POST.get("username")
        roombuilding = request.POST.get("pk")
        room = RoomServer.objects.get(buildingRoom=roombuilding)
        room.delete()
        rooms = RoomServer.objects.filter(user__username=user)
        data['form_is_valid'] = True
        data['html_room_list']= render_to_string('adminall/room/roomAdminlist.html',{'room':rooms,'username':user})
    else:
        context={'room':roombuilding,'user':user}
        data['html_room_form']= render_to_string('adminall/room/deleteroom.html',context=context,request=request)
    return JsonResponse(data)

#profile admin
def adminProfile(request):
    user = request.user
    profile = request.user.userprofile
    form = ProfileForm(instance=user)
    forms = ProfilePic(instance=profile)
    if request.method =="POST":
        form= ProfileForm(request.POST,instance=user)
        forms= ProfilePic(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
        if forms.is_valid():
            forms.save()
    content={'form':form,'forms':forms}
    return render (request,"adminall/profile/profileadmin.html",content)

#adminPassword
def passwordAdmin(request):
    data= dict()
    user= request.user
    form_reset=resetPasswordForm(data=request.POST,user=user)
    if form_reset.is_valid():
        form_reset.save()
        data['form_is_valid']=True
    else:
        data['form_is_valid']=False
    data['html_list'] = render_to_string("adminall/profile/changepass.html",{'form_reset':form_reset},request=request)
    return JsonResponse(data)

#search card
def searchcard(request):
    user = request.GET.get("user") or None
    data= dict()
    username=None
    if user is not None:
        username = User.objects.filter(username__icontains=user)
    else:
        username= User.objects.all()
    data['html_list'] = render_to_string("adminall/adminpage.html",{'user':username},request=request)
    return JsonResponse(data)

#get history
def searchdateadmin(request):
    data = dict()
    dat= list()
    room=None
    roomid = request.GET.get("date_and_day") or None
    user = request.GET.get("user") or None
    if roomid is not None:
        roomid = datetime.datetime.strptime(roomid,'%Y-%m-%d').date()
    temperature = TemperatureStore.objects.all()
    if temperature.exists():
        if user is not None and roomid is not None:
            for i in temperature:
                if roomid == i.date and user == i.room.user.username:
                    dat.append(i)
        elif roomid is not None and user is None:
            for i in temperature:
                if roomid == i.date:
                    dat.append(i)
        elif roomid is None and user is not None:
            for i in temperature:
                if user == i.room.user.username:
                    dat.append(i)
    paginator = Paginator(dat,5)
    page = request.GET.get('page',1)
    try:
        room = paginator.page(page)
    except PageNotAnInteger:
        room = paginator.page(1)
    except EmptyPage:
        room = paginator.page(paginator.num_pages)
    data['html_list']=render_to_string("adminall/history/historylist.html",{'room':room},request=request)
    data['html_pagination']=render_to_string("adminall/history/pagination.html",{'room':room},request=request)
    return JsonResponse(data)

#userpage
def userpage(request):
    user = User.objects.all().order_by('-id')
    paginator = Paginator(user,5)
    page = request.GET.get('page',1)
    try:
        room = paginator.page(page)
    except PageNotAnInteger:
        room = paginator.page(1)
    except EmptyPage:
        room = paginator.page(paginator.num_pages)
    return render(request,"adminall/user/user.html",{"username":room})

#search user
def searchUser(request):
    data= dict()
    username=request.GET.get("username")
    user = User.objects.filter(username__icontains=username).order_by('-id')
    paginator = Paginator(user,5)
    page = request.GET.get('page',1)
    try:
        user = paginator.page(page)
    except PageNotAnInteger:
        user = paginator.page(1)
    except EmptyPage:
        user = paginator.page(paginator.num_pages)
    content={
        'username':user,
    }
    data['html_list']= render_to_string("adminall/user/userlist.html",context=content,request=request)
    return JsonResponse(data)

#Edit user
def editUser(request,pk):
    data=dict()
    form,forms=None,None
    user = User.objects.filter(pk=pk)
    if user.exists():
        user = User.objects.get(pk=pk)
        form = editUserForm(instance=user)
        forms = phoneForm(instance=user.userprofile)
    if request.method =="POST":
        form = editUserForm(request.POST, instance=user)
        forms =phoneForm(request.POST,instance=user.userprofile)
        if form.is_valid() or forms.is_valid():
            emaildata = form.cleaned_data.get("email")
            email = User.objects.filter(email=emaildata)
            if email.exists():
                data['form_is_valid']=False 
            else:
                data['form_is_valid']=True
                form.save()
            data['form_is_valid']=True
            forms.save()
            user = User.objects.all().order_by('-id')
            paginator = Paginator(user,5)
            page = request.GET.get('page',1)
            try:
                room = paginator.page(page)
            except PageNotAnInteger:
                room = paginator.page(1)
            except EmptyPage:
                room = paginator.page(paginator.num_pages)
            data['html_list']=render_to_string("adminall/user/userlist.html",{"username":room},request=request)
        else:
            data['form_is_valid']=False
    content={'form':form,'forms':forms}
    data['html_form_list']= render_to_string("adminall/user/useredit.html",context=content,request=request)
    return JsonResponse(data)
# delete user
def deleteUser(request):
    data=dict()
    pk= request.GET.get("pk")
    user = User.objects.filter(pk=pk)
    if user.exists():
        user =User.objects.get(pk=pk)
    if request.method=="POST":
        pk= request.POST.get("pk")
        data['form_is_valid']=True
        user= User.objects.get(pk=pk)
        user.delete()
        user = User.objects.all().order_by('-id')
        paginator = Paginator(user,5)
        page = request.GET.get('page',1)
        try:
            room = paginator.page(page)
        except PageNotAnInteger:
            room = paginator.page(1)
        except EmptyPage:
            room = paginator.page(paginator.num_pages)
        data['html_list']=render_to_string("adminall/user/userlist.html",{"username":room},request=request)
    else:
        data["form_is_valid"]=False
    content={
        'user':user,
    }
    data['html_form_list']= render_to_string("adminall/user/userdelete.html",context=content,request=request)
    return JsonResponse(data)