from adminpage.views import (
    User,userProfile,render_to_string,
    render,Group,login_required,unanthenticated_user
    ,allow_subadmins,admin_only,Avg,JsonResponse
    ,Q)
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from adminpage.forms import choiceForm_weekly,choiceForm_annually,choiceForm_monthly


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
    room = request.GET.get("room")
    form = choiceForm_weekly(request.POST or None)
    print(room)
    if form.is_valid():
        template_path="subadmin/generatereport/pdfweek.html"
        print(room)
        
    data['html_list']=render_to_string("subadmin/generatereport/weekform.html",{'form':form},request=request)
    return JsonResponse(data)
def generateMonthlyForm(request):
    data=dict()
    room = request.GET.get("room")
    form = choiceForm_monthly(request.POST or None)
    print(room)
    if form.is_valid():
        template_path="subadmin/generatereport/pdfymonth.html"
        print(room)
        
    data['html_list']=render_to_string("subadmin/generatereport/monthform.html",{'form':form},request=request)
    return JsonResponse(data)
def generateAnnuallyForm(request):
    data=dict()
    room = request.GET.get("room")
    form = choiceForm_annually(request.POST or None)
    print(room)
    if form.is_valid():
        
        data['form_is_valid'] =True
        template_path="subadmin/generatereport/pdfyear.html"
        
    else:
        data['form_is_valid']=False
    data['html_list']=render_to_string("subadmin/generatereport/yearform.html",{'form':form},request=request)
    return JsonResponse(data)

#pdf for all like month year and weekly
def render_to_pdf(template_path,context):
    response = HttpResponse(content_type = 'application/pdf')
    filename= "Report_.pdf"
    response['Content-Disposition'] = 'attachment; filename=%s'%(filename)
    template = get_template(template_path)
    html = template.render(context)
    pisaStatus =pisa.CreatePDF(
        html,dest=response,link_callback=link_callback)
    if pisaStatus.err:
        return JsonResponse(context)
    