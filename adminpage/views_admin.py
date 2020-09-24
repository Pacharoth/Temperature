from adminpage.views import (
    User,userProfile,render_to_string,messages,
    render,Group,login_required,unanthenticated_user
    ,allow_subadmins,admin_only,Avg,JsonResponse
    ,Q,datetime)
from adminpage.models import TemperatureStore
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from adminpage.forms import choiceForm_weekly,choiceForm_annually,choiceForm_monthly
from adminpage.utils import weekList,monthList,annuallyList

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
    print(room)
    if form.is_valid():
        data['form_is_valid']=True
        template_path="generatereport/pdfymonth.html"
        print(room)
        
    else:
        data['form_is_valid'] = False
    data['html_list']=render_to_string("generatereport/monthform.html",{'form':form},request=request)
    return JsonResponse(data)
def generateAnnuallyForm(request):
    data=dict()
    room = request.GET.get("room")
    form = choiceForm_annually(request.POST or None)
    print(room)
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