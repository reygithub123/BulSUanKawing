from braces.views import UserPassesTestMixin, LoginRequiredMixin
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.views import PasswordChangeView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http.response import HttpResponse, HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.views import generic
from django.views.decorators.http import require_GET, require_POST
from PIL import Image as Im

#self imports

from announcements.models import *
from organization.models import Organization, Program
from authorization.forms import *
from cal.forms import *
from document_collection.forms import UploadFileForm
from document_collection.models import *
from events.models import *
from events.forms import *
from gallery.models import *
from gallery.forms import *
from workspace.models import *
from workspace.forms import * 

#form imports
from .forms import *
from authorization.forms import PasswordChangingForm

#emailing stuff
from bulsuankawing.settings import EMAIL_HOST_USER
from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

#download/upload files stuff
import os
import zipfile
from io import StringIO,BytesIO
import re
from pathlib import Path

#calendar stuff

import calendar
import datetime
from cal.utils import Calendar
from datetime import date, datetime, timedelta

#dashboard
@login_required()
@staff_member_required()
def view_cms_dashbord(request):
    #get general info
    logged_in = request.user.id;
    org = Organization.objects.get(user_id=logged_in)
    org = get_object_or_404(Organization, user_id=logged_in)
    info = GeneralInformation.objects.all().first()
    title = info.name_acronym +" CMS"
    logoupload = ChangeLogoForm(instance=info)
    
    if request.method=="POST":
        genform = GeneralInformationForm(request.POST, instance =info )
        if genform.is_valid():
            genform.save()
            messages.info(request,"<p class='info w-100'>&#9432; <em>Update Successful</em></p>")
    else: 
        genform = GeneralInformationForm(instance=info)
    
    
    context = {
        "org":org,
        'info':info,
        'genform':genform,
        'logoupload':logoupload,
        'title':title,
    }
    return render (request, "gen_info/content-management-system.html",context)


@login_required()
@staff_member_required()
@require_POST
def change_logo(request):
    #get general info
    logged_in = request.user.id
    org = Organization.objects.get(user_id=logged_in)
    org = get_object_or_404(Organization, user_id=logged_in)
    info = GeneralInformation.objects.all().first()
    if request.method =="POST":
        logoupload = ChangeLogoForm(request.POST, request.FILES,instance=info)
        if logoupload.is_valid():
            logoupload.save()
            org.logo = request.FILES['logo']
            org.save()
        else:
            messages.info(request,f"<p class='error w-100'>&#9888; Form Error {logoupload.errors.as_text} </p>" )
        
    return redirect ("cms:cms_land")

#account
@login_required()
@staff_member_required()
def view_cms_account_setup(request):
    #get general info
    logged_in = request.user.id;
    org = Organization.objects.get(user_id=logged_in)
    org = get_object_or_404(Organization, user_id=logged_in)
    info = GeneralInformation.objects.all().first()
    title = info.name_acronym +" Account"
    
    
    if request.method=="POST":
        accform = EditAccountForm(request.POST, instance =request.user )
        if accform.is_valid():
            accform.save()
            messages.info(request,"<p class='info w-100'>&#9432; <em>Update Successful</em></p>")
    else: 
        accform = EditAccountForm(instance=request.user)
    
    
    context = {
        "org":org,
        'info':info,
        'accform':accform,
        'title':title,
    }
    return render (request, "gen_info/account-setup.html",context)



class PasswordsChangeView(UserPassesTestMixin,LoginRequiredMixin, PasswordChangeView  ):
    form_class = PasswordChangingForm
    success_url = reverse_lazy("cms:password-success")
    template_name ="gen_info/password-setup.html"
    def test_func(self,user):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        #get general info
        logged_in = self.request.user.id
        org = Organization.objects.get(user_id=logged_in)
        org = get_object_or_404(Organization, user_id=logged_in)
        info = GeneralInformation.objects.all().first()
        title = info.name_acronym +" Account"
        
        context = super().get_context_data(**kwargs)
        context['org_id']=mark_safe(org.id)
        context['org'] = org
        context['info'] = info
        context['title'] = mark_safe(title)
        return context


@login_required()
@staff_member_required()
def  redirect_success_change_pass(request):
    messages.info(request, "<p class = 'info'>&#9432; Password Changed Succesfully</p>")
    return redirect('cms:view-passwords')
    

#documents

@login_required()
@staff_member_required()
def view_pending_documents(request):
    #get general info
    logged_in = request.user.id;
    org = Organization.objects.get(user_id=logged_in)
    org = get_object_or_404(Organization, user_id=logged_in)
    info = GeneralInformation.objects.all().first()
    title = "Documents"
    
    
    states = EventState.objects.all()
    pendingstate = EventState.objects.filter(status ='Pending').first()
    approvedstate = EventState.objects.filter(status ='Approved').first()
    declinedstate = EventState.objects.filter(status ='Declined').first()
    
    documentslist = DocumentCollection.objects.filter(state=pendingstate).order_by('-id')
    state=pendingstate
    #filter by state
    gotstate=request.GET.get("state")
    if gotstate != None:
        if gotstate == "None":
            state = "None"
        else:
            state = EventState.objects.get(id=gotstate)

        
    
    if state != None :
        if state == "None":
            documentslist = DocumentCollection.objects.all()
            state="None"
        else:
            documentslist = DocumentCollection.objects.filter(state = state).order_by('-id')
    
    searched = request.GET.get("searched")
    if searched !=None:
        documentslist = documentslist.filter(Q(name__contains=searched)
                                           |Q(state__status__contains=searched)
                                           |Q(category__name__in=searched)
                                           |Q(src_ID__name__in=searched)
                                           )
    
    orglist=[]
    for doc in documentslist:
        source = doc.src_ID
        orglist.append(source) if source not in orglist else orglist
    
    #paging
    p = Paginator(orglist, 10)
    page_number = request.GET.get('page')
    
    try:
        orgs = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        orgs = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        orgs = p.page(p.num_pages)
    context = {
        "org":org,
        'info':info,
        'title':title,
        'orgs':orgs,
        'states':states,
        'currentstate':state,
    }
    return render (request, "cms_docs/orgslist.html",context)


@login_required()
@staff_member_required()
def view_org_documents(request, org_id):
    #get general info
    logged_in = request.user.id
    org = Organization.objects.get(user_id=logged_in)
    org = get_object_or_404(Organization, user_id=logged_in)
    
    current_org_doc = Organization.objects.get(id=org_id)
    title = current_org_doc.acronym+" Submitted Documents"
      
    states = EventState.objects.all()
    pendingstate = EventState.objects.filter(status ='Pending').first()
    approvedstate = EventState.objects.filter(status ='Approved').first()
    declinedstate = EventState.objects.filter(status ='Declined').first()
    #filter by state
    documentlist = DocumentCollection.objects.filter(src_ID = current_org_doc.id).order_by('-state').order_by('-submitted')
    
    state=pendingstate
    gotstate=request.GET.get("state")
    if gotstate != None:
        if gotstate == "All":
            state = "All"
        else:
            state = EventState.objects.get(id=gotstate)
            
    if state != None :
        if state == "All":
            documentlist = DocumentCollection.objects.filter(src_ID = current_org_doc.id).order_by('-submitted')
            state="All"
        else:
            documentlist = DocumentCollection.objects.filter(src_ID = current_org_doc.id,state = state).order_by('-submitted')
    
    
    
    category = request.GET.get("filter")
    searched = request.GET.get("searched")
    
    if category != None and category !="All":
        documentlist = documentlist.filter(category = category).order_by('-state').order_by('-submitted')
        state="All"
        current_category = Category.objects.get(id=category)
    else:
        category="All"
        current_category = category
        
    
    if searched !=None:
        documentlist = DocumentCollection.objects.filter(Q(name__contains=searched)
                                           |Q(state__status__contains=searched)
                                           |Q(category__name__in=searched)
                                           )
   
    selected_org = Organization.objects.get(id=org_id)
    categories = Category.objects.all()
    #paging
    p = Paginator(documentlist, 20)
    page_number = request.GET.get('page')
    
    try:
        documents = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        documents = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        documents = p.page(p.num_pages)
    
    context = {
        "title":title,
        "org":org,
        "documents":documents,
        "categories":categories,
        "searched":searched,
        "filter":category,
        'states':states,
        'currentstate':state,
        'approved':approvedstate,
        'current_org':selected_org,
        'current_category':current_category,
        'all':'All',
        
    }
    return render (request, "cms_docs/documents.html",context)

@login_required()
@staff_member_required()
def view_selected_document(request, org_id, doc_id):
    #get general info
    logged_in = request.user.id;
    org = Organization.objects.get(user_id=logged_in)
    org = get_object_or_404(Organization, user_id=logged_in)
    info = GeneralInformation.objects.all().first()
    title = info.name_acronym +" Account"
    
    states = EventState.objects.all()
    pendingstate = EventState.objects.filter(status ='Pending').first()
    approvedstate = EventState.objects.filter(status ='Approved').first()
    declinedstate = EventState.objects.filter(status ='Declined').first()
    
    uploadfileform = UploadFileForm()
    documentcollection = DocumentCollection.objects.get(id = doc_id)
    fileslist = Document.objects.filter(collection = documentcollection, state = documentcollection.state).order_by('id')
    
    approved_state = EventState.objects.get(status = "Approved")
   
    selected_org = Organization.objects.get(id=org_id)
    title = documentcollection
    context = {
        "title":title,
        "org":org,
        "files":fileslist,
        "document":documentcollection,
        'uploadfile': uploadfileform,
        'approved':approved_state,
        'current_org':selected_org,
        'approved':approvedstate,
        'declined':declinedstate,
        'pending':pendingstate,
    }
    return render (request, "cms_docs/document.html",context)



@login_required()
@staff_member_required()
@require_POST
def receive_document(request, org_id, doc_id):
    
    documentcollection = DocumentCollection.objects.get(id = doc_id)
    fileslist = Document.objects.filter(collection = documentcollection, state = documentcollection.state).order_by('id')
    if fileslist:
            
        subdir = str(documentcollection)
        subdir =re.sub('[^A-Za-z0-9]+', '', subdir)

        # Files (local path) to put in the .zip
        # FIXME: Change this (get paths from DB etc)
        filenames=[]
        for file in fileslist:
            dir = str(file.file).replace("\"", "\\")
            BASE=Path(__file__).resolve().parent.parent
            filenames.append(os.path.join(BASE,f"media\\{dir}"))
            print(f"{BASE}{dir}")
        

        # Folder name in ZIP archive which contains the above files
        # E.g [thearchive.zip]/somefiles/file2.txt
        # FIXME: Set this to something better
        zip_subdir = str(subdir)
        zip_filename = "%s.zip" % zip_subdir

        # Open StringIO to grab in-memory ZIP contents
        s = BytesIO()

        # The zip compressor
        zf = zipfile.ZipFile(s, "w")

        for fpath in filenames:
            # Calculate path for file in zip
            fdir, fname = os.path.split(fpath)
            zip_path = os.path.join(zip_subdir, fname)

            # Add file, at correct path
            zf.write(fpath, zip_path)

        # Must close zip for all contents to be written
        zf.close()

        # Grab ZIP file from in-memory, make response with correct MIME-type
        resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
        # ..and correct content-disposition
        resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

        return resp
    else:
        messages.info(request,"<p class='info'>&#9432; No Documents to Receive</p>")
        return redirect(f"/cms/documents/{org_id}/{doc_id}/")
#sample email template send

    
@login_required()
@staff_member_required()
@require_POST
def return_document_email(request,org_id,doc_id):
    if request.method=="POST":
        
        
        #get general info
        info = GeneralInformation.objects.all().first()
        pendingstate = EventState.objects.filter(status ='Pending').first()
        approvedstate = EventState.objects.filter(status ='Approved').first()
        declinedstate = EventState.objects.filter(status ='Declined').first()
        
        
        
        isfiled = request.POST.get('filed')
        message = request.POST.get('message')
        state = EventState.objects.get(id =request.POST.get('status') )
        
        org = Organization.objects.get(user_id=org_id)
        user = org.user
        
        documentcollection = DocumentCollection.objects.get(id = doc_id)
        
        documentcollection.message = message
        
        documentcollection.state = state
        
        documentcollection.save()
        
        if documentcollection.event:
            
            event = documentcollection.event
            event.state= documentcollection.state
            event.save()
            
        if isfiled:
            
            orgname = org.acronym
            orgname = re.sub('[^A-Za-z0-9]+', '', orgname)
            
            docname = documentcollection.name
            
            docname = re.sub('[^A-Za-z0-9]+', '', docname)
            folder = orgname+"/"+docname 
            BASE_PATH='media/document_collections'
        
            try:
                os.makedirs(os.path.join(BASE_PATH, folder))
                
            except:
                pass
            if request.method =="POST":
                
                files = request.FILES.getlist('files')
                for doc in files:
                    full_filename = os.path.join(BASE_PATH, folder, doc.name)
                    dbfilename = os.path.join("document_collections/",folder,doc.name)
                    handle_uploaded_file(full_filename, doc)
                    file = Document.objects.create(
                        collection = documentcollection,
                        name = doc.name,
                        file=dbfilename ,
                        state = documentcollection.state
                    )
        else:
            files = Document.objects.filter(collection = documentcollection)
            for file in files:
                file.state=documentcollection.state
                file.save()
        #create message
        
        title_message= ""
        inmessage=""
        if pendingstate==state or declinedstate==state:
            title_message="Your Files Need Revision"
            inmessage=f"The documents for {documentcollection.name} needs some revision. Your document is <strong>{state}</strong>"
        elif approvedstate==state:
            title_message="Congratulations!"
            inmessage=f"The documents for {documentcollection.name} is now <strong>{state}</strong>"
        
        html_content = render_to_string("cms_docs/return_document_template.html",{
            'title':'Document Returned',
            "info":info,
            'title_message':title_message,
            'inmessage':inmessage,
            'message':message,
            })
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(
            documentcollection.name,
            text_content,
            EMAIL_HOST_USER,
            [user.email, 'bulsuankawing@gmail.com']
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
    return redirect(f"/cms/documents/{org_id}/{doc_id}/")


def handle_uploaded_file(file_name,f):
    destination = open(file_name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    return

#CMS Calendar
class CMSCalendarView( UserPassesTestMixin,LoginRequiredMixin,generic.ListView):
    model = Event
    template_name = 'cms_ev/calendar.html'
    def test_func(self,user):
        
        return self.request.user.is_staff

    def get_context_data(self ,**kwargs):
        context = super().get_context_data(**kwargs)
        #import kwargs values
         #get general info
        logged_in = self.request.user.id
        org = Organization.objects.get(user_id=logged_in)
        org = get_object_or_404(Organization, user_id=logged_in)
        info = GeneralInformation.objects.all().first() 
        
        context['org_id']=mark_safe(org.id)
        context['org'] = org
        context['title'] = mark_safe("BulSUan Kawing Events")
        context['info'] = mark_safe(info)
        
        
        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))

        # Instantiate calendar class with today's year and date
        cal = Calendar(d.year, d.month)
        
        # Call the formatmonth method, which returns our calendar as a table
        eventview=4 #event view as admin
        html_cal = cal.formatmonth(False,eventview,withyear=True)
        context['calendar'] = mark_safe(html_cal)

        # call previous or next month
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        
        

        return context
    
    
def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


@login_required()
@staff_member_required()
def view_events(request):
     #get general info
    logged_in = request.user.id
    org = Organization.objects.get(user_id=logged_in)
    org = get_object_or_404(Organization, user_id=logged_in)
    title = "All Events"
    info = GeneralInformation.objects.all().first() 
    
    pending_state = EventState.objects.get(status = "Pending")
    approved_state = EventState.objects.get(status = "Approved")
    #events of org and components

    searched = request.GET.get('searched')
    if searched:
        events_list = Event.objects.all().order_by('-time_begin')
        events_list = events_list.filter(Q(title__contains=searched)
                            |Q(src_ID__acronym__contains=searched)
                            |Q(src_ID__name__contains = searched)
                            )
    else:
        events_list = Event.objects.all().order_by('-time_begin')
        searched=False
    
    #paging
    p = Paginator(events_list,12)
    page_number = request.GET.get('page')
    
    try:
        events = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        events = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        events = p.page(p.num_pages)
    
    context ={
        'title': title,
        'searched': searched,
        'org': org,
        'info':info,
        'events': events,
        'pending':pending_state,
        'approved':approved_state,
        'searched': searched,
    }
    return render(request, 'cms_ev/events.html', context)

@login_required()
@staff_member_required()
def view_add_event(request):
    #get general info
    logged_in = request.user.id
    org = Organization.objects.get(user_id=logged_in)
    org = get_object_or_404(Organization, user_id=logged_in)
    title = "Add Event"
    info = GeneralInformation.objects.all().first() 
    
    
    errors = ""
    messages=""
    invalid = False
    if request.method =="POST":
        src_ID=request.POST.get('src_ID')
        evname=request.POST.get('title')
        time_begin = request.POST.get('time_begin')
        time_end = request.POST.get('time_end')
        description = request.POST.get('description')
        state = request.POST.get('state')
        image = request.FILES.get('img_src')
        
        pending_state = EventState.objects.get(status = "Pending")
        
        data ={
            'src_ID':src_ID,
            'title':evname,
           'time_begin': time_begin,
           'time_end': time_end,
           'description': description,
           'state': state,
           
           }
        if time_begin > time_end:
            invalid = True;
            errors +="<p class = 'errors'>&#x26A0; Time Begin is greater than Time end</p><br>"
        if evname == None  or time_begin == None or time_end == None or image == None:
            invalid = True
            errors += "<p class = 'errors'>&#x26A0; Please fill up empty fields</p><br>"
        if invalid:
            eventform = AddCMSEventForm(initial = data )
            addimg = AddEventImageForm(initial = {'image': image,})
            context = {
                "title":title,
                "org":org,
                'eventform':eventform,
                'addimg': addimg,
                'errors': errors,
                'invalid': invalid,
                'info':info,
                
            }
            return render (request, "cms_ev/add-event.html",context)
        else:
            imagecol = ImageCollection.objects.create(
                img_src = image,
            )
            event = Event.objects.create(
                src_ID_id = src_ID,
                title = evname,
                time_begin = time_begin,
                time_end=time_end,
                description = description,
                img_ID = imagecol,
                state_id = state ,
                                         )
            messages += "<p class = 'info'>&#9432; Event Successfully Added</p><br>"
    
    eventform = AddCMSEventForm()
    addimg = AddEventImageForm()
    
    context = {
        "title":title,
        "org":org,
        'eventform':eventform,
        'addimg': addimg,
        'errors': errors,
        'invalid': invalid,
        'info':info,
        'messages':messages,
        
    }
    return render (request, "cms_ev/add-event.html",context)

@login_required()
@staff_member_required()
def view_edit_event(request, ev_id):
    #get general info
    logged_in = request.user.id
    org = Organization.objects.get(user_id=logged_in)
    org = get_object_or_404(Organization, user_id=logged_in)
    
    errors = ""
    invalid = False
    event = get_object_or_404(Event,  id=ev_id)
    currentorg = event.src_ID
    
    title = event.title 
    try:
        document = DocumentCollection.objects.get(event = event.id)
    except DocumentCollection.DoesNotExist:
        document = False
        
    eventform = AddCMSEventForm(instance=event)
    addimg = EditEventImageForm()
    
    data ={
        'title':event.title,
        'time_begin': event.time_begin,
        'time_end': event.time_end,
        'description': event.description,
    }
    if request.method =="POST":
        evname=request.POST.get('title')
        time_begin = request.POST.get('time_begin')
        time_end = request.POST.get('time_end')
        description = request.POST.get('description')
        image = request.FILES.get('img_src')
        state = request.POST.get('state')
        pending_state = EventState.objects.get(status = "Pending")
        activity_cat = Category.objects.get(name="Activities")
        data ={
            
            'title':evname,
            'time_begin': time_begin,
            'time_end': time_end,
            'description': description,   
        }
        if time_begin > time_end:
            invalid = True;
            errors +="<p class = 'errors'>Error: Time Begin is greater than Time end</p><br>"
        if evname == None  or time_begin == None or time_end == None :
            invalid = True
            errors += "<p>Error: Please fill up empty fields</p><br>"
        if invalid:
            eventform = AddEventForm(request.POST,initial=data,instance=event )
            
            addimg = EditEventImageForm(initial = {'image': image,})
            context = {
               "title":title,
                "org":org,
                'eventform':eventform,
                'addimg': addimg,
                'errors': errors,
                'invalid': invalid,
                'event': event,
                'currentorg':currentorg,
            }
            return render (request, "cms_ev/edit-event.html",context)
        else:
            eventform = AddEventForm(request.POST, instance = event)
            eventform.src_ID=event.src_ID
            if eventform.is_valid():
                if image:
                    imagecol = ImageCollection.objects.create(img_src = image)
                    event.img_ID = imagecol
                
                status = EventState.objects.get(id=state)
                event.state = status
                event.save()
                eventform.save()
                return redirect("cms:view-events")
            else:
                print(eventform.errors)
            
   
    
    context = {
        "title":title,
        "org":org,
        'eventform':eventform,
        'addimg': addimg,
        'errors': errors,
        'invalid': invalid,
        'event': event,
        'document':document,
        'currentorg':currentorg,
    }
    return render (request, "cms_ev/edit-event.html",context)

#event ajax
@login_required()
@staff_member_required()
@require_POST
def view_delete_event(request):
    
    logged_in = request.user.id
    if request.method =="POST":
        id = request.POST.get("id")
        event = get_object_or_404(Event,  id=id)
        event.delete()
    return HttpResponse ("")


#organizations

@login_required()
@staff_member_required()
def view_organizations(request):
    #get general info
    logged_in = request.user.id
    org = Organization.objects.get(user_id=logged_in)
    org = get_object_or_404(Organization, user_id=logged_in)
    title="Organizations"
    
    info = GeneralInformation.objects.all().first() 
    organizations = Organization.objects.filter(~Q(state="o")).order_by('name')
    pendingorg = Organization.objects.filter(state="p").count()
    
    categories= TypesOfOrganization.objects.filter(~Q(name="OSOA")).order_by('name')
    searched = request.GET.get('searched')
    filter = request.GET.get('filter')
    if searched:
        organizations = organizations.filter(
                                            Q(name__contains=searched)
                                            |Q(acronym__contains=searched)
                                            |Q(program__name__contains = searched)
                                            |Q(program__acronym__contains = searched)
                                            |Q(program__college__contains = searched)
                                            |Q(program__college_acronym__contains = searched)
                                            |Q(category__name__contains = searched)
                                            )
        print("searched")
    else:
        searched=False
    if filter and filter != "All" and not searched:
        organizations =  organizations.filter(
                                            Q(category__id__contains= filter)
                                            |Q(state= filter)
                                            ).order_by('name')
        
    p = Paginator(organizations, 12)
    page_number = request.GET.get('page')
    
    try:
        orgs = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        orgs = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        orgs = p.page(p.num_pages)
    

    context = {
        "title":title,
        "org":org,
        "orgs":orgs,
        "pendingorg":pendingorg,
        "categories":categories,
        'searched': searched,
        'filter':filter,
        "info":info,
        
    }
    return render (request, "cms_orgs/search-organization.html",context)




@login_required()
@staff_member_required()
def view_organization(request, org_id):
     #get general info
    logged_in = request.user.id
    org = Organization.objects.get(user_id=logged_in)
    org = get_object_or_404(Organization, user_id=logged_in)
    
    info = GeneralInformation.objects.all().first() 
    
    programs = Program.objects.all()
    orgtypes = TypesOfOrganization.objects.all().filter(~Q(name="OSOA")).order_by('name')
    
    organization = get_object_or_404(Organization, id=org_id)
    events = Event.objects.filter(src_ID=organization)[:3]
    title= organization.acronym
    messages=False
    if request.method=="POST":
        orgtype = request.POST.get('orgtype')
        program = request.POST.get('program')
        state = request.POST.get('state')
        orgtypeclass = TypesOfOrganization.objects.get(id=orgtype)
        programclass = Program.objects.get(id=program)

        organization.program=programclass
        organization.category=orgtypeclass
        organization.state=state
        organization.save()
        messages=f"<p class='info'>&#9432; {organization.acronym} successfully validated</p>"
    context = {
        "title":title,
        "org":org,
        "organization":organization,
        'info':info,
        "events":events,
        "programs":programs,
        "orgtypes":orgtypes,
        "messages":messages,
    }
    
    return render (request, "cms_orgs/selected-org.html",context)

@login_required()
@staff_member_required()
def view_organization_events(request, org_id):
    #get general info
    logged_in = request.user.id
    org = Organization.objects.get(user_id=logged_in)
    org = get_object_or_404(Organization, user_id=logged_in)
    title = "All Events"
    info = GeneralInformation.objects.all().first() 
    
    pending_state = EventState.objects.get(status = "Pending")
    approved_state = EventState.objects.get(status = "Approved")
    #events of org and components
    current_org = Organization.objects.get(id=org_id)
    events_list = Event.objects.filter(src_ID=current_org).order_by('-time_begin')
    searched = request.GET.get('searched')
    if searched:
        events_list = events_list.filter(Q(title__contains=searched)
                            |Q(src_ID__acronym__contains=searched)
                            |Q(src_ID__name__contains = searched)
                            )
    else:
        
        events_list = Event.objects.filter(src_ID=org_id).order_by('-time_begin')
        searched=False
    
    #paging
    p = Paginator(events_list,12)
    page_number = request.GET.get('page')
    
    try:
        events = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        events = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        events = p.page(p.num_pages)
    context ={
        'title': title,
        'searched': searched,
        'org': org,
        'info':info,
        'events': events,
        'pending':pending_state,
        'approved':approved_state,
        'searched': searched,
        'currentorg':current_org,
    }
    return render(request, 'cms_orgs/ev/events.html', context)



#view gallery
@login_required()
@staff_member_required()
def view_gallery(request, *args, **kwargs):
     #get general info
    logged_in = request.user.id
    org = Organization.objects.get(user_id=logged_in)
    org = get_object_or_404(Organization, user_id=logged_in)
    title = org.acronym +" Gallery"
    
    #get Gallery
    albums = Album.objects.filter(src_ID = org.id).order_by('-last_modified')
    

    context ={
        'title': title,
        'albums': albums,
        'org': org,
    }
    return render(request, 'cms_gallery/gallery.html', context)

@login_required()
@staff_member_required()
def view_album(request, album_id):
     
    #get general info
    logged_in = request.user.id
    org = Organization.objects.get(user_id=logged_in)
    org = get_object_or_404(Organization, user_id=logged_in)
    title = org.acronym +" Gallery"
    
    #get Album
    album = Album.objects.get(pk = album_id)
    
    #get Album Images
    images = Image.objects.filter(album = album_id)
    context ={
        'title': title,
        'images': images,
        'album': album,
        'org': org,
    }
    
    return render(request, 'cms_gallery/album.html', context)

@login_required()
@require_POST
@staff_member_required()
def add_album(request):
    #get general info
    logged_in = request.user.id
    org = Organization.objects.get(user_id=logged_in)
    org = get_object_or_404(Organization, user_id=logged_in)
    
    orgname = org.acronym
    orgname = re.sub('[^A-Za-z0-9]+', '', orgname)
    
    name = request.POST.get("name")
    cover = request.FILES["cover"]
    if not name or not cover:
    
        error = "Album Creation Failed"
        return redirect ("org:view-gallery")
    
    
    
    albumname = re.sub('[^A-Za-z0-9]+', '', name)
    folder = orgname+"/"+albumname 
    BASE_PATH='media/gallery'
   
    try:
        os.makedirs(os.path.join(BASE_PATH, folder))
        
    except:
        pass
    
    full_filename = os.path.join(BASE_PATH, folder, cover.name)
    dbfilename = os.path.join("gallery/",folder,cover.name)
    handle_uploaded_file(full_filename, cover)
    newalbum = Album.objects.create(src_ID_id= org.id,name=name, key_image=dbfilename)

    return redirect("cms:view-album",  newalbum.id)

    
@login_required()
@require_POST
@staff_member_required()
def view_upload_images(request,album_id):
    logged_in = request.user.id
    org = Organization.objects.get(user_id=logged_in)
    
    orgname = org.acronym
    orgname = re.sub('[^A-Za-z0-9]+', '', orgname)
    
    album = Album.objects.get(id = album_id)
    albumname = album.name
    
    albumname = re.sub('[^A-Za-z0-9]+', '', albumname)
    folder = orgname+"/"+albumname 
    BASE_PATH='media/gallery'
   
    try:
        os.makedirs(os.path.join(BASE_PATH, folder))
        
    except:
        pass
    if request.method =="POST":
        
        files = request.FILES.getlist('file')
        for img in files:
            full_filename = os.path.join(BASE_PATH, folder, img.name)
            dbfilename = os.path.join("gallery/",folder,img.name)
            handle_uploaded_file(full_filename, img)
            image = Image.objects.create(
                album = album,
                image=dbfilename,
                name = img.name
            )
    return redirect("cms:view-album", album_id)

@login_required()
@require_POST
@staff_member_required()
def delete_images(request, album_id):
    if request.method =="POST":
        ids = request.POST.getlist("images")
        print (ids)
        for id in ids:
            img = Image.objects.get(id=id)
            img.delete()
    return redirect ("cms:view-album", album_id)


@login_required()
@require_POST
@staff_member_required()
def delete_album(request):
    if request.method =="POST":
        id = request.POST.get("id")
        album = Album.objects.get(id=id)
        album.delete()
    return HttpResponse ("")


@login_required()
@require_POST
@staff_member_required()
def rename_album(request, album_id):
    if request.method =="POST":
        id = request.POST.get("id")
        name = request.POST.get("name")
        col = Album.objects.get(id=id)
        col.name = name
        col.save()
    return HttpResponse ("")

#news

@login_required()
@staff_member_required()
def view_news(request):
     #get general info
    logged_in = request.user.id
    org = Organization.objects.get(user_id=logged_in)
    org = get_object_or_404(Organization, user_id=logged_in)
    title = "News"
    info = GeneralInformation.objects.all().first() 
    
    #events of org and components

    searched = request.GET.get('searched')
    if searched:
        news = Announcement.objects.all().order_by('-published')
        news = news.filter(Q(title__contains=searched)
                            )
    else:
        news = Announcement.objects.all().order_by('-published')
        searched=False
    
    #paging
    p = Paginator(news,12)
    page_number = request.GET.get('page')
    
    try:
        news = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        news = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        news = p.page(p.num_pages)
    
    context ={
        'title': title,
        'searched': searched,
        'org': org,
        'info':info,
        'news': news,
        'searched': searched,
    }
    return render(request, 'cms_news/news.html', context)

@login_required()
@staff_member_required()
def view_add_news(request):
    #get general info
    logged_in = request.user.id
    org = Organization.objects.get(user_id=logged_in)
    org = get_object_or_404(Organization, user_id=logged_in)
    title = "Add News"
    info = GeneralInformation.objects.all().first() 
    
    
    errors = ""
    messages=""
    invalid = False
    if request.method =="POST":
        title=request.POST.get('title')
        published = request.POST.get('published')
        description = request.POST.get('description')
        image = request.FILES.get('img_src')
        
        data ={
            'title':title,
           'published': published,
           'description': description,
           
           }
        
        if invalid:
            newsform = NewsForm(initial = data )
            addimg = AddEventImageForm(initial = {'image': image,})
            context = {
                "title":title,
                "org":org,
                'newsform':newsform,
                'addimg': addimg,
                'errors': errors,
                'invalid': invalid,
                'info':info,
                
            }
            return render (request, "cms_news/add-news.html",context)
        else:
            imagecol = ImageCollection.objects.create(
                img_src = image,
            )
            news = Announcement.objects.create(
               
                title = title,
                published = published,
                description = description,
                img_ID = imagecol,
                                         )
            messages += "<p class = 'info'>&#9432; News Successfully Added</p><br>"
    
    newsform = NewsForm()
    addimg = AddEventImageForm()
    
    context = {
        "title":title,
        "org":org,
        'newsform':newsform,
        'addimg': addimg,
        'errors': errors,
        'invalid': invalid,
        'info':info,
        'messages':messages,
        
    }
    return render (request, "cms_news/add-news.html",context)

@login_required()
@staff_member_required()
def view_edit_news(request, ev_id):
    #get general info
    logged_in = request.user.id
    org = Organization.objects.get(user_id=logged_in)
    org = get_object_or_404(Organization, user_id=logged_in)
    
    errors = ""
    invalid = False
    news = get_object_or_404(Announcement,  id=ev_id)

    
    title = news.title 
    
    newsform = NewsForm(instance=news)
    
    
    messages=False
    if request.method =="POST":
        newtitle=request.POST.get('title')
        published = request.POST.get('published')
        description = request.POST.get('description')
        image = request.FILES.get('img_src')
        
        data ={
            'title':newtitle,
           'published': published,
           'description': description,
           
           }
        
        if invalid:
            newsform = NewsForm(request.POST,initial=data,instance=news )
            context = {
               "title":newtitle,
                "org":org,
                'newsform':newsform,
                'errors': errors,
                'invalid': invalid,
            }
            return render (request, "cms_ev/edit-event.html",context)
        else:
            newsform = NewsForm(request.POST, instance = news)
            
            if newsform.is_valid():
                if image:
                    imagecol = ImageCollection.objects.create(img_src = image)
                    news.img_ID = imagecol
                news.save()
                newsform.save()
                messages = "<p class = 'info'>&#9432; News Successfully Updated</p><br>"
            else:
                print(newsform.errors)
            
   
    
    context = {
        "title":title,
        "org":org,
        'newsform':newsform,
        'errors': errors,
        'invalid': invalid,
        'news': news,
        'messages': messages,
    }
    return render (request, "cms_news/edit-news.html",context)

#event ajax
@login_required()
@staff_member_required()
@require_POST
def view_delete_news(request):
    
    logged_in = request.user.id
    if request.method =="POST":
        id = request.POST.get("id")
        news = get_object_or_404(Announcement,  id=id)
        news.delete()
    return HttpResponse ("")


#oso officers

@login_required()
@staff_member_required()
def view_officers(request):
    
    #get general info
    logged_in = request.user.id
    org = Organization.objects.get(user_id=logged_in)
    org = get_object_or_404(Organization, user_id=logged_in)
    info = GeneralInformation.objects.all().first()
    title = info.name_acronym+ " Officers"
    
    head = Officer.objects.all().filter(hierarchy=0)
    leaders = Officer.objects.all().filter(hierarchy=1)
    primary = Officer.objects.all().filter(hierarchy=2)
    secondary = Officer.objects.all().filter(hierarchy=3)
    others = Officer.objects.all().filter(hierarchy=4)
    
    
    context ={
        'title': title,
        'org': org,
        'info':info,
        'head': head,
        'leaders': leaders,
        'primary': primary,
        'secondary': secondary,
        'others': others,
        
        }
    return render (request, "cms_officers/officers.html",context)
    

@login_required()
@staff_member_required()
def view_add_officer(request):
    
    #get general info
    logged_in = request.user.id
    org = Organization.objects.get(user_id=logged_in)
    org = get_object_or_404(Organization, user_id=logged_in)
    info = GeneralInformation.objects.all().first()
    title = "Add Officer"
    
    officerform = OfficerForm()
    message=False
    if request.method =="POST":
        officerform = OfficerForm(request.POST)
        if officerform.is_valid():
            officerform.save()
            officerform = OfficerForm()
            message="<p class='info'>&#9432; Officer added successfully</p>"
   
    
    context ={
        'title': title,
        'org': org,
        'info':info,
        'officerform':officerform,
        'message':message,
        
        }
    return render (request, "cms_officers/add-officer.html",context)


@login_required()
@staff_member_required()
def view_edit_officer(request,of_id):
    #get general info
    logged_in = request.user.id
    org = Organization.objects.get(user_id=logged_in)
    org = get_object_or_404(Organization, user_id=logged_in)
    info = GeneralInformation.objects.all().first()
    officer =Officer.objects.get(id=of_id)
    
    title = officer.name
    
    officerform = OfficerForm(instance=officer)
    message=False
    if request.method =="POST":
        officerform = OfficerForm(request.POST,instance=officer)
        if officerform.is_valid():
            officerform.save()
            officerform = OfficerForm(instance=officer)
            message="<p class='info'>&#9432; Officer saved successfully</p>"
   
    
    context ={
        'title': title,
        'org': org,
        'info':info,
        'officerform':officerform,
        'message':message,
        'officer': officer,
        
        }
    
    return render (request, "cms_officers/edit-officer.html",context)
#officer ajax


@login_required()
@staff_member_required()
@require_POST
def view_delete_officer(request):
    logged_in = request.user.id
    if request.method =="POST":
        id = request.POST.get("id")
        news = get_object_or_404(Officer,  id=id)
        news.delete()
    return HttpResponse ("")