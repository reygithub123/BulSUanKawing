
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from braces.views import UserPassesTestMixin, LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.db.models import Q
from django.http.response import HttpResponse, HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.utils.safestring import mark_safe
from django.views import generic
from django.views.decorators.http import require_GET, require_POST


#direct imports

import calendar
import datetime
import os
import re

#utils
from cal.utils import Calendar
from datetime import date, datetime, timedelta

from information.models import TypesOfOrganization

#self imports
from .models import Organization
from authorization.forms import *
from cal.forms import *
from document_collection.forms import UploadFileForm
from document_collection.models import *
from events.models import *
from events.models import *
from events.forms import *
from gallery.models import *
from gallery.forms import *
from workspace.models import *
from workspace.forms import *

def is_org(user):
    try:
        org = Organization.objects.get(user_id=user.id)
        
        if  org.state=="s":
            return False
        if not user.is_staff:
            return True
        else:
            return False
    except Organization.DoesNotExist:
        return False
def is_setup(user):
    try:
        org = Organization.objects.get(user_id=user.id)
        if  org.state=="s":
            return True
        else:
            return redirect ("org:view-dashboard")
    except Organization.DoesNotExist:
        return False


@login_required()
@user_passes_test(is_setup)
def view_account_setup(request):
    title = "Organizational Account Setup"
    logged_in = request.user.id
    org = Organization.objects.get(user_id=logged_in)
    org = get_object_or_404(Organization, user_id=logged_in)
    if org.state != 's':
        return redirect ("org:view-dashboard")
    if request.method =="POST":
        orgform = EditOrgForm(request.POST,request.FILES,instance=org)
        
        if orgform.is_valid():
            org.state = 'p'
            org.save()
            workspace = Workspace.objects.create(src_ID=org, name = org.name +" Workspace")
            workspace.save()
            orgform.save()
            return render (request, "setup/welcome-message.html",{'title':title})
    else: 
        orgform = EditOrgForm()
    
    
    context = {
        "title":title,
        "org":org,
        "orgform":orgform,
    }
    return render (request, "setup/organization-data.html",context)


@login_required()
@user_passes_test(is_org)
def view_org_dashboard(request):
    
    #get general info
    logged_in = request.user.id
    org = Organization.objects.get(user_id=logged_in)
    org = get_object_or_404(Organization, user_id=logged_in)
    title = "Welcome, " + org.acronym +"!"
    
    events = Event.objects.filter(src_ID = org.id).order_by('-time_begin')[:3]
    pendingstate = 'p' 
    
    universityorg= TypesOfOrganization.objects.get(name="University Wide Organization")
    collegeorg= TypesOfOrganization.objects.get(name="College Based Organization")
    context = {
        "title":title,
        "org":org,
        "events":events,
        'pendingstate': pendingstate,
        'universityorg': universityorg,
        'collegeorg': collegeorg,
    }
    return render (request, "org-dashboard.html",context)


@login_required()
@user_passes_test(is_org)
def view_org_settings(request):
    
    #get general info
    logged_in = request.user.id
    org = Organization.objects.get(user_id=logged_in)
    org = get_object_or_404(Organization, user_id=logged_in)
    title = "Welcome, " + org.acronym +"!"
    orgform = EditOrgForm(instance = org)
    orgeditform = EditSettingOrgForm(instance=org)
    accountform = EditUserForm(instance= request.user)
    
    context = {
        "title":title,
        "org":org,
        'orgform':orgform,
        'orgeditform':orgeditform,
        'accountform': accountform,
    }
    return render (request, "settings1.html",context)

@login_required()
@require_POST
@user_passes_test(is_org)
def profile_upload(request):
    #get general info
    logged_in = request.user.id
    org = Organization.objects.get(user_id=logged_in)
    org = get_object_or_404(Organization, user_id=logged_in)
    
    if request.method =="POST":
        org.logo = request.FILES['logo']
        org.save()
        
    return redirect ("org:view-me")

@login_required()
@require_POST
@user_passes_test(is_org)
def profile_update(request):
    #get general info
    logged_in = request.user.id
    org = Organization.objects.get(user_id=logged_in)
    org = get_object_or_404(Organization, user_id=logged_in)
    
    if request.method =="POST":    
        orgform = EditSettingOrgForm(request.POST,instance=org)
        if orgform.is_valid():
            orgform.save()
        else:
            messages.error(request, "&#9888;"+orgform.errors.as_text())
    return redirect ("org:view-me")

@login_required()
@require_POST
@user_passes_test(is_org)
def account_update(request):
    #get general info
    logged_in = request.user.id
    
    if request.method =="POST":    
        accform = EditUserForm(request.POST,instance=request.user)
        if accform.is_valid():
            accform.save()
            messages.info(request,"<p class = 'info'>&#9432; Account Update Successful</p>")
        else:
           messages.error(request,accform.errors.as_ul())
    return redirect ("org:view-me")
@login_required()
@user_passes_test(is_org)
def view_org_documents(request):
    #get general info
    logged_in = request.user.id
    org = Organization.objects.get(user_id=logged_in)
    org = get_object_or_404(Organization, user_id=logged_in)
    title = org.acronym +" Submitted Documents"
    
    documentlist = DocumentCollection.objects.filter(src_ID = org.id).order_by('-submitted')
    
    approved_state = EventState.objects.get(status = "Approved")
   
    
    category = request.GET.get("filter")
    searched = request.GET.get("searched")
    if category != None and category !="None":
        documentlist = documentlist.filter(category = category)
    if searched !=None:
        documentlist = documentlist.filter(Q(name__contains=searched)
                                           |Q(state__status__contains=searched)
                                           |Q(category__name__in=searched)
                                           )
    categories = Category.objects.all()
    state = EventState.objects.filter(~Q(status="No Document")
                                      |~Q(status="OSOA"))
    
    #paging
    p = Paginator(documentlist, 10)
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
        "state":state,
        "searched":searched,
        "filter":category,
        'approved':approved_state,
    }
    return render (request, "org_documents/documents.html",context)
@login_required()
@user_passes_test(is_org)
def view_open_document(request,doc_id):
    #get general info
    logged_in = request.user.id
    org = Organization.objects.get(user_id=logged_in)
    org = get_object_or_404(Organization, user_id=logged_in)

    uploadfileform = UploadFileForm()
    documentcollection = DocumentCollection.objects.get(id = doc_id)
    fileslist = Document.objects.filter(collection = documentcollection, state = documentcollection.state).order_by('-id')
    
    approved_state = EventState.objects.get(status = "Approved")
   
    
    title = documentcollection.name
    context = {
        "title":title,
        "org":org,
        "files":fileslist,
        "document":documentcollection,
        'uploadfile': uploadfileform,
        'approved':approved_state,
    }
    return render (request, "org_documents/submitted-documents.html",context)

#view gallery
@login_required()
@user_passes_test(is_org)
def view_org_gallery(request, *args, **kwargs):
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
    return render(request, 'org_gallery/gallery.html', context)

@login_required()
@user_passes_test(is_org)
def view_org_album(request, album_id):
     
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
    
    return render(request, 'org_gallery/album.html', context)

@login_required()
@require_POST
@user_passes_test(is_org)
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

    return redirect("org:view-album",  newalbum.id)

    
@login_required()
@require_POST
@user_passes_test(is_org)
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
    return redirect("org:view-album", album_id)

@login_required()
@require_POST
@user_passes_test(is_org)
def delete_images(request, album_id):
    if request.method =="POST":
        ids = request.POST.getlist("images")
        print (ids)
        for id in ids:
            img = Image.objects.get(id=id)
            img.delete()
    return redirect ("org:view-album", album_id)


@login_required()
@require_POST
@user_passes_test(is_org)
def view_upload_file(request,doc_id):
    logged_in = request.user.id
    org = Organization.objects.get(user_id=logged_in)
    
    orgname = org.acronym
    orgname = re.sub('[^A-Za-z0-9]+', '', orgname)
    
    documentcollection = DocumentCollection.objects.get(id = doc_id)
    docname = documentcollection.name
    
    docname = re.sub('[^A-Za-z0-9]+', '', docname)
    folder = orgname+"/"+docname 
    BASE_PATH='media/document_collections'
   
    try:
        os.makedirs(os.path.join(BASE_PATH, folder))
        
    except:
        pass
    if request.method =="POST":
        
        files = request.FILES.getlist('file')
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
    return redirect("org:view-document", doc_id)

@login_required()
@require_POST
@user_passes_test(is_org)
def view_change_file(request,doc_id):
    logged_in = request.user.id
    org = Organization.objects.get(user_id=logged_in)
    
    orgname = org.acronym
    orgname = re.sub('[^A-Za-z0-9]+', '', orgname)
    
    documentcollection = DocumentCollection.objects.get(id = doc_id)
    docname = documentcollection.name
    
    docname = re.sub('[^A-Za-z0-9]+', '', docname)
    folder = orgname+"/"+docname 
    BASE_PATH='media/document_collections'
   
    try:
        os.makedirs(os.path.join(BASE_PATH, folder))
        
    except:
        pass
    if request.method =="POST":
        file_id = request.POST.get("id")
        doc = request.FILES['file']

        full_filename = os.path.join(BASE_PATH, folder, doc.name)
        dbfilename = os.path.join("document_collections/",folder,doc.name)
        handle_uploaded_file(full_filename, doc)
        file = Document.objects.get(
            id = file_id,
        )
        file.file=dbfilename
        file.name=str(doc)
        file.save()
    return redirect("org:view-document", doc_id)

def handle_uploaded_file(file_name,f):
    destination = open(file_name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    return

@login_required()
@user_passes_test(is_org)
def view_org_workspace(request):
    
    #get general info
    logged_in = request.user.id
    org = Organization.objects.get(user_id=logged_in)
    org = get_object_or_404(Organization, user_id=logged_in)
    title =org.acronym +" Workspace"
    
    workspace = Workspace.objects.filter(src_ID = org.id).first()
    works = ToDoList.objects.all().filter(wp_ID = workspace.id).order_by('order')
    tasks = Task.objects.all().filter(tdl_ID__wp_ID= workspace.id).order_by('state')
    
     #forms
    addform = WorkForm(request.POST or None)
    if request.method =="POST":
        addform = WorkForm(request.POST)
        if addform.is_valid():
            #specify workspace id
            addform.cleaned_data['wp_ID_id']=workspace.id
            new = ToDoList.objects.create(**addform.cleaned_data)
            tdl_id = new.id
            return redirect(f"org:view-edit-work", tdl_id)
            
    
    context = {
        "title":title,
        "org":org,
        "workspace": workspace,
        "works": works,
        "tasks": tasks,
        
        "addform": addform,
    }
    
    return render (request, "workspace/workspace.html",context)

@login_required()
@user_passes_test(is_org)
def view_org_edit_work(request, tdl_id):
    
    #get general info
    logged_in = request.user.id
    org = Organization.objects.get(user_id=logged_in)
    org = get_object_or_404(Organization, user_id=logged_in)
    
    workspace = Workspace.objects.filter(src_ID = org.id).first()
    
    current = datetime.datetime.now()
   
    work = ToDoList.objects.filter(pk = tdl_id).first()
    work = get_object_or_404(ToDoList, pk = tdl_id)
    tasks = Task.objects.filter(tdl_ID= work.id).order_by('made')
    states = TaskState.objects.all()
    
    #forms
    workform = WorkForm(initial = {'name':work.name, 'order': work.order, 'color': work.color})
    
    data ={'state':'1'}
    
    taskform = TaskForm(initial=data)
    
    if request.method =="POST":
        workform = WorkForm(request.POST)
        if workform.is_valid():
            work = ToDoList.objects.filter(pk = tdl_id).first()
            work.name = workform.cleaned_data['name']
            work.order = workform.cleaned_data['order']
            work.color = workform.cleaned_data['color']
            work.save(update_fields =['name', 'order', 'color'])
            workform = WorkForm()
            return redirect("org:view-workspace")
   
    title = "Edit Work"
        
    context = {
        "title":title,
        "org":org,
        "workspace": workspace,
        "work": work,
        "tasks": tasks,
        "workform": workform,
        "taskform": taskform,
        "states":states,
        "current":current,
    }
    
    return render (request, "workspace/edit-work.html",context)

@login_required()
@user_passes_test(is_org)
def view_add_event(request):
    #get general info
    logged_in = request.user.id
    org = Organization.objects.get(user_id=logged_in)
    org = get_object_or_404(Organization, user_id=logged_in)
    title ="Add Event for "+ org.acronym
    
    errors = ""
    invalid = False
    if request.method =="POST":
        evname=request.POST.get('title')
        time_begin = request.POST.get('time_begin')
        time_end = request.POST.get('time_end')
        description = request.POST.get('description')
        image = request.FILES.get('img_src')
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
            errors +="<p class = 'errors'>&#x26A0; Time Begin is greater than Time end</p><br>"
        if evname == None  or time_begin == None or time_end == None or image == None:
            invalid = True
            errors += "<p>&#x26A0; Please fill up empty fields</p><br>"
        if invalid:
            eventform = AddEventForm(initial = data )
            addimg = AddEventImageForm(initial = {'image': image,})
            context = {
                "title":title,
                "org":org,
                'eventform':eventform,
                'addimg': addimg,
                'errors': errors,
                'invalid': invalid,
                
            }
            return render (request, "ev/add-event.html",context)
        else:
            imagecol = ImageCollection.objects.create(
                img_src = image,
            )
            event = Event.objects.create(
                src_ID = org,
                title = evname,
                time_begin = time_begin,
                time_end=time_end,
                description = description,
                img_ID = imagecol,
                state = pending_state ,
                                         )
            document = DocumentCollection.objects.create(
                src_ID = org,
                name = event.title +" Approval",
                category = activity_cat,
                event = event,
                state = pending_state,
            )
            return redirect("org:view-document", document.id)
        
        
    else:
        eventform = AddEventForm()
        addimg = AddEventImageForm()
    
    context = {
        "title":title,
        "org":org,
        'eventform':eventform,
        'addimg': addimg,
        'errors': errors,
        'invalid': invalid,
        
        
    }
    return render (request, "ev/add-event.html",context)

@login_required()
@user_passes_test(is_org)
def view_edit_event(request, ev_id):
    #get general info
    logged_in = request.user.id
    org = Organization.objects.get(user_id=logged_in)
    org = get_object_or_404(Organization, user_id=logged_in)
    
    errors = ""
    invalid = False
    event = get_object_or_404(Event, src_ID=org, id=ev_id)
    try:
        document = DocumentCollection.objects.get(event = event.id)
    except DocumentCollection.DoesNotExist:
        document = False

    title =event
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
            eventform = AddEventForm(initial = data )
            addimg = EditEventImageForm(initial = {'image': image,})
            context = {
               "title":title,
                "org":org,
                'eventform':eventform,
                'addimg': addimg,
                'errors': errors,
                'invalid': invalid,
                'event': event,
            }
            return render (request, "ev/edit-event.html",context)
        else:
            eventform = AddEventForm(request.POST, instance = event)
            if image:
                imagecol = ImageCollection.objects.create(img_src = image)
                event.img_ID = imagecol
                event.save()
            eventform.save()
            return redirect("org:view-events")
    else:
        eventform = AddEventForm(instance=event)
        addimg = EditEventImageForm()
    
    context = {
        "title":title,
        "org":org,
        'eventform':eventform,
        'addimg': addimg,
        'errors': errors,
        'invalid': invalid,
        'event': event,
        'document':document,
    }
    return render (request, "ev/edit-event.html",context)


@login_required()
@require_POST
@user_passes_test(is_org)
def add_doc(request, ev_id):
    eventid = request.POST.get('event')
    print (str(eventid)== str(ev_id))
    if str(eventid) == str(ev_id):
        logged_in = request.user.id
        org = Organization.objects.get(user_id=logged_in)
        event = Event.objects.get(id = eventid)
        pending_state = EventState.objects.get(status = "Pending")
        activity_cat = Category.objects.get(name="Activities")
        document = DocumentCollection.objects.create(
            
            src_ID = org,
            name = event.title +" Approval",
            category = activity_cat,
            event = event,
            state = pending_state,
             
        )
        event.state=pending_state
        event.save()
        return redirect("org:view-document", document.id)
    else:
        return redirect ('org:view-events')


@login_required()
@user_passes_test(is_org)
def view_org_events(request):
     #get general info
    logged_in = request.user.id
    org = Organization.objects.get(user_id=logged_in)
    org = get_object_or_404(Organization, user_id=logged_in)
    title = org.acronym +" Events"
    
    pending_state = EventState.objects.get(status = "Pending")
    approved_state = EventState.objects.get(status = "Approved")
    #events of org and components
    if request.method =="POST":
        searched = request.POST['searched']
        
        events_list = Event.objects.filter(src_ID = org.id).order_by('-time_begin')
        events_list = events_list.filter(Q(title__contains=searched)
                           |Q(src_ID__acronym__contains=searched)
                           |Q(src_ID__name__contains = searched)
                           )
    else:
        events_list = Event.objects.filter(src_ID = org.id).order_by('-time_begin')
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
        'events': events,
        'pending':pending_state,
        'approved':approved_state,
    }
    return render(request, 'ev/events.html', context)

#Class views
#Organizational Calendar
class CalendarView( UserPassesTestMixin,LoginRequiredMixin,generic.ListView):
    model = Event
    template_name = 'ev/cal/calendar.html'
    def test_func(self,user):
        try:
            org = Organization.objects.get(user_id=self.request.user.id)
            if not self.request.user.is_staff:
                return True
            else:
                return False
        except Organization.DoesNotExist:
            return False

    def get_context_data(self ,**kwargs):
        context = super().get_context_data(**kwargs)
        #import kwargs values
         #get general info
        logged_in = self.request.user.id
        org = Organization.objects.get(user_id=logged_in)
        org = get_object_or_404(Organization, user_id=logged_in)

        context['org_id']=mark_safe(org.id)
        context['org'] = org
        context['title'] = mark_safe(org.acronym+" Events")
        
        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))

        # Instantiate calendar class with today's year and date
        cal = Calendar(d.year, d.month)
        
        # Call the formatmonth method, which returns our calendar as a table
        eventview=3 #event view only as org level
        html_cal = cal.formatmonth(org.id,eventview,withyear=True)
        context['calendar'] = mark_safe(html_cal)

        # call previous or next month
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        
        

        return context

class PasswordsChangeView(UserPassesTestMixin,LoginRequiredMixin, PasswordChangeView  ):
    form_class = PasswordChangingForm
    success_url = reverse_lazy("org:password-success")
    def test_func(self,user):
        try:
            org = Organization.objects.get(user_id=self.request.user.id)
            if not self.request.user.is_staff:
                return True
            else:
                return False
        except Organization.DoesNotExist:
            return False
    def get_context_data(self, **kwargs):
        #get general info
        logged_in = self.request.user.id
        org = Organization.objects.get(user_id=logged_in)
        org = get_object_or_404(Organization, user_id=logged_in)
        context = super().get_context_data(**kwargs)
        context['org_id']=mark_safe(org.id)
        context['org'] = org
        context['title'] = mark_safe("Change Password")
        return context

        
    
def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.datetime.today()


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

@login_required
@user_passes_test(is_org)
def  redirect_success_change_pass(request):
    messages.info(request, "<p class = 'info'>&#9432; Password Changed Succesfully</p>")
    return redirect('org:view-me')


#ajaxified

@login_required()
@require_POST
@user_passes_test(is_org)
def delete_album(request):
    if request.method =="POST":
        id = request.POST.get("id")
        album = Album.objects.get(id=id)
        album.delete()
    return HttpResponse ("")


@login_required()
@require_POST
@user_passes_test(is_org)
def rename_album(request, album_id):
    if request.method =="POST":
        id = request.POST.get("id")
        name = request.POST.get("name")
        col = Album.objects.get(id=id)
        col.name = name
        col.save()
    return HttpResponse ("")

@login_required()
@user_passes_test(is_org)
@require_POST
def view_delete_event(request):
    
    logged_in = request.user.id
    if request.method =="POST":
        id = request.POST.get("id")
        org = get_object_or_404(Organization, user_id=logged_in)
        event = get_object_or_404(Event, src_ID=org, id=id)
        event.delete()
    return HttpResponse ("")


@login_required()
@user_passes_test(is_org)
@require_POST
def view_delete_document(request):
    
    if request.method =="POST":
        id = request.POST.get("id")
        coll = DocumentCollection.objects.get(id=id)
        
        nodoc_state = EventState.objects.get(status = "No Document")
        if coll.event:
            event = Event.objects.get(id = coll.event.id)
            event.state=nodoc_state
            event.save()
        coll.delete()
    return HttpResponse ("")


@login_required()
@user_passes_test(is_org)
@require_POST
def view_rename_doc(request, doc_id):
    
    if request.method =="POST":
        id = request.POST.get("id")
        name = request.POST.get("name")
        col = DocumentCollection.objects.get(id=id)
        col.name = name
        col.save()
    return HttpResponse ("")


@login_required()
@user_passes_test(is_org)
@require_POST
def view_delete_file(request, doc_id):
    
    if request.method =="POST":
        id = request.POST.get("id")
        doc = Document.objects.get(id=id)
        doc.delete()
    return HttpResponse ("")



@login_required()
@user_passes_test(is_org)
@require_POST
def view_submit_document(request):
     #get general info
    logged_in = request.user.id
    org = Organization.objects.get(user_id=logged_in)
    org = get_object_or_404(Organization, user_id=logged_in)
    pendingstate = EventState.objects.filter(status="Pending").first()
    
    name = request.POST.get("name")
    category = request.POST.get("category")
    newdoc = DocumentCollection.objects.create(src_ID_id= org.id,name=name, category_id=category, state=pendingstate)
    doc_id = newdoc.id
    return redirect("org:view-document", doc_id)


@login_required()
@user_passes_test(is_org)
@require_POST
def view_rename_wp(request):
    
    if request.method =="POST":
        id = request.POST.get("id")
        name = request.POST.get("name")
        workspace = Workspace.objects.get(id=id)
        workspace.name = name
        workspace.save()
    return HttpResponse ("")



@login_required()
@user_passes_test(is_org)
@require_POST
def view_delete_work(request):
    
    if request.method =="POST":
        id = request.POST.get("id")
        tdl = ToDoList.objects.get(id=id)
        tdl.delete()
    return HttpResponse ("")


@login_required()
@user_passes_test(is_org)
@require_POST
def view_add_task(request, tdl_id):
    
    if request.method =="POST":
        taskform =TaskForm(request.POST)
        taskform.full_clean()    
        if taskform.is_valid():
            taskform.save()
        else:
            print(taskform.errors)
    return HttpResponse ("")

@login_required()
@user_passes_test(is_org)
@require_POST
def view_task_changestate(request,tdl_id, task_id):
    
    
    if request.method == "POST":
        state = request.POST['state']
        task = Task.objects.get(id=task_id)
        task.state_id = state
        task.save()
        
    return HttpResponse ("")


@login_required()
@user_passes_test(is_org)
def view_org_edit_task(request, tdl_id, task_id):
    task = Task.objects.get(pk=task_id)
    task = get_object_or_404(Task,pk=task_id)
    states = TaskState.objects.all()
    data ={'name':task.name,
           'description':task.description,
           'time_begin':task.time_begin,
           'time_end':task.time_end,
           'state':task.state.id,
           
           }
    taskform = TaskForm(initial=data)
    
    context = {
        'taskform':taskform,
        "states":states,
        'initialstate':task.state.id,
        "task": task,
    }
    
    if request.method=="GET":
        return render (request, "workspace/modal-edit-task.html",context)
    elif request.method =="POST":
        taskform =TaskForm(request.POST, instance=task)
        if taskform.is_valid():
            taskform.save()
            return render (request, "workspace/modal-edit-task.html",context)
        else:
            print(taskform.errors)
        
    
    return HttpResponseNotFound()  
    

        
@login_required()
@user_passes_test(is_org)
@require_POST
def view_org_delete_task(request, tdl_id, task_id):
    task = Task.objects.get(pk=task_id)
    task = get_object_or_404(Task,pk=task_id)
    
    if request.method =="POST":
        task.delete()
        
    
    return HttpResponse ("")
    

        