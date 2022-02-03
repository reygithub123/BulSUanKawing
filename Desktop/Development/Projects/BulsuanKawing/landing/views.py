from django.core.mail import send_mail
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from cal.utils import Calendar
import calendar
from datetime import date, datetime, timedelta
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q 
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.safestring import mark_safe
from django.views import generic


#my models
from announcements.models import Announcement
from events.models import Event, EventState
from images.models import ImageCollection
from information.models import GeneralInformation,TypesOfOrganization, Officer
from organization.models import Organization, Program
from gallery.models import Album, Image

#my forms
from cal.forms import EventForm

def view_homepage(request, *args, **kwargs):
    
    #title
    title ="BulSUan Kawing"
    
    #set GeneralInformation
    info = GeneralInformation.objects.all()[:1]
    
    for inf in info:
        office_name = inf.office_name
        acronym = inf.name_acronym
        about = inf.about
        about2 =False
        logo = inf.logo
        if len(about) > 500:
            about2 = about[:500]+"..."
    
    #call upcoming events
    states = EventState.objects.all()
    imgs = ImageCollection.objects.all()
    for st in states:
        if st.status == 'OSOA':
            state=st.id
    event_list = Event.objects.filter(state=state).order_by('-time_begin')[:3]
    
    evval1, evval2,evval3 = True,True,True
    event1, event2, event3 = False, False, False
    evimages = []
    if event_list:
        events=True
        for event in event_list:
            if len(event.description) > 100:
                event.description = event.description[0:200]+"..."
            evimages.append(imgs.get(id=event.img_ID_id).img_src)
            if evval1:
                event1=event
                evval1=False
                continue
            elif not evval1 and not event1:
                event1=False
                evval1=False
                
            if evval2:
                event2=event
                evval2=False
                continue
            elif not evval2 and not event2:
                event2=False
                evval2=False
                
            if evval3:
                event3=event
                evval3=False
                continue
            elif not evval3 and not event3:
                event3=False
                evval3=False
    else:
        events=False;
    #call announcements
    announcements_list = Announcement.objects.all().order_by('-published')[:4]
    animages= []
    
    if announcements_list:
        announcements = True
        for ann in announcements_list:
            animages.append(imgs.get(id=ann.img_ID_id).img_src)
            
    else:
        announcements=False
    
    successmessage =None
    # Emailing 
    if request.method =='POST':
        topic = request.POST['topic']
        email = request.POST['email']
        message = request.POST['message']
        successmessage="<p class='successmessage'>Email Successfully Sent!<p><p='sublabel'> We will respond to you shortly. </p"
        send_mail(
            #subject
            topic + " from " +email,
            #message
            message,
            #from email
            email,
            #to email 
            ['bulsuankawing@gmail.com'],
        )
        request.method="GET"
    context ={
        'title':title,
        'office_name': office_name,
        'acronym': acronym,
        'about': about,
        'logo': logo,
        'about2': about2,
        
        'event1': event1,
        'event2': event2,
        'event3': event3,
        'images': evimages,
        'events': events,
        'new_announcements': announcements_list,
        'animages': animages,
        'announcements': announcements,
        'successmessage':successmessage,
        
    }
    
    return render(request, 'homepage.html', context)



def view_events(request, *args, **kwargs):
    
    #title
    title ="OSOA Events"
    
    #set GeneralInformation
    info = GeneralInformation.objects.all()[:1]
    
    for inf in info:
        office_name = inf.office_name
        acronym = inf.name_acronym
        logo = inf.logo
    
    #events and components
    if request.method =="POST":
        searched = request.POST['searched']
        
        events_list = Event.objects.all().order_by('-time_begin')
        events_list = events_list.filter(Q(title__contains=searched))
    else:
        events_list = Event.objects.all().order_by('-time_begin')
        searched=False
    
    #paging
    p = Paginator(events_list, 12)
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
    'title':title,
    'office_name': office_name,
    'acronym': acronym,
    'logo': logo,
    'events': events,
    
    }

    
    return render(request, 'articles/events.html', context)

def view_event(request,event_id=None):
    #title
    title ="OSOA Events"
    
    #set GeneralInformation
    info = GeneralInformation.objects.all()[:1]
    
    for inf in info:
        office_name = inf.office_name
        acronym = inf.name_acronym
        logo = inf.logo
    
    #get Event
    event = Event
    if event_id:
        event = get_object_or_404(Event, pk=event_id)
    else:
        event = Event
    

    title = event.title
    context={
        'title':title,
        'office_name': office_name,
        'acronym': acronym,
        'logo': logo,
        'event':event,
    }
    return render(request, 'articles/event-view.html', context)


def view_news(request, *args, **kwargs):
    
    #title
    title ="News & Updates"
    
    #set GeneralInformation
    info = GeneralInformation.objects.all()[:1]
    
    for inf in info:
        office_name = inf.office_name
        acronym = inf.name_acronym
        logo = inf.logo
    #news and components
    if request.method =="POST":
        searched = request.POST['searched']
        
        news_list = Announcement.objects.all().order_by('-published')
        news_list = news_list.filter(Q(title__contains=searched))
    else:
        news_list = Announcement.objects.all().order_by('-published')
        searched=False
    
    #paging
    p = Paginator(news_list, 12)
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
    'title':title,
    'office_name': office_name,
    'acronym': acronym,
    'logo': logo,
    'news': news,
    
    }

    
    return render(request, 'articles/news/news.html', context)

def view_news_info(request,news_id=None):
    
    
    #set GeneralInformation
    info = GeneralInformation.objects.all()[:1]
    
    for inf in info:
        office_name = inf.office_name
        acronym = inf.name_acronym
        logo = inf.logo
    
    #get Event
    news = Announcement
    if news_id:
        news = get_object_or_404(Announcement, pk=news_id)
    else:
        news = Announcement
    

    title = news.title
    context={
        'title':title,
        'office_name': office_name,
        'acronym': acronym,
        'logo': logo,
        'news':news,
    }
    return render(request, 'articles/news/news-view.html', context)
def view_about_bk(request):
    #title
    title ="About | BulSUan Kawing"
    #set GeneralInformation
    info = GeneralInformation.objects.all()[:1]
    
    for inf in info:
        office_name = inf.office_name
        acronym = inf.name_acronym
        logo = inf.logo

    
    context ={
        'title': title,
        'office_name': office_name,
        'acronym': acronym,
        'logo': logo,
 
        }
    return render(request, 'about/about_bk.html',context)
    
def view_about_oso(request,*args,**kwargs):
    #title
    title ="About | BulSUan Kawing"
    #set GeneralInformation
    info = GeneralInformation.objects.all()[:1]
    orgtypes = TypesOfOrganization.objects.exclude(name="OSOA")
    
    #officers
    head = Officer.objects.all().filter(hierarchy=0)
    leaders = Officer.objects.all().filter(hierarchy=1)
    primary = Officer.objects.all().filter(hierarchy=2)
    secondary = Officer.objects.all().filter(hierarchy=3)
    others = Officer.objects.all().filter(hierarchy=4)
    
    numoforg = len(orgtypes)
    for inf in info:
        office_name = inf.office_name
        acronym = inf.name_acronym
        description = inf.description
        description2 = False
        history = inf.history
        history2 =False
        logo = inf.logo
        if len(description) > 500:
            description2 = description[:500]+"..."
        if len(history) > 500:
            history2 = history[:500]+"..."
    
    context ={
        'title': title,
        'office_name': office_name,
        'acronym': acronym,
        'description': description,
        'description2': description2,
        'history': history,
        'history2': history2,
        'logo': logo,
        'orgtypes': orgtypes,
        'numoforg': numoforg,
        'head': head,
        'leaders': leaders,
        'primary': primary,
        'secondary': secondary,
        'others': others,
        }
    return render(request, 'about/about.html',context)

def view_gallery(request, *args, **kwargs):
     
    #title
    title ="Gallery | BulSUan Kawing"
    
    #set GeneralInformation
    info = GeneralInformation.objects.all()[:1]
    for inf in info:
        office_name = inf.office_name
        acronym = inf.name_acronym
        logo = inf.logo
    #get Org
    
    #get Gallery
    albums = Album.objects.filter(admin = True).order_by('-last_modified')
    

    context ={
        'title': title,
        'office_name': office_name,
        'acronym': acronym,
        'logo': logo,
        'albums': albums,
    }
    return render(request, 'articles/gallery/gallery.html', context)

def view_album(request, album_id, *args, **kwargs):
     
    #title
    
    #set GeneralInformation
    info = GeneralInformation.objects.all()[:1]
    for inf in info:
        office_name = inf.office_name
        acronym = inf.name_acronym
        logo = inf.logo
    
    #get Album
    album = Album.objects.get(pk = album_id)
    
    title =f"{album} | BulSUan Kawing"
    #get Album Images
    images = Image.objects.filter(album = album_id)
    context ={
        'title': title,
        'office_name': office_name,
        'acronym': acronym,
        'logo': logo,
        'images': images,
        'album': album,
    }
    
    return render(request, 'articles/gallery/album.html', context)
    



#view organizations
def view_search(request,  *args, **kwargs):
    
    #title
    title ="Organizations | BulSUan Kawing"
    #set GeneralInformation
    info = GeneralInformation.objects.all()[:1]
    
    for inf in info:
        office_name = inf.office_name
        acronym = inf.name_acronym
        logo = inf.logo
        
    #organizations and components
    if request.method =="POST":
        searched = request.POST['searched']
        
        orgs = Organization.objects.filter(state='r')
        orgs = orgs.filter(Q(name__contains=searched)
                           |Q(acronym__contains=searched)
                           |Q(program__name__contains = searched)
                           |Q(program__acronym__contains = searched)
                           |Q(program__college__contains = searched)
                           |Q(category__name__contains = searched)
                           )
    else:
        orgs = Organization.objects.filter(state='r')
        searched=False
    
    p = Paginator(orgs, 12)
    page_number = request.GET.get('page')
    
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    context = {'page_obj': page_obj}
    
    
    context ={
        'title':title,
        'page_obj':page_obj,
        'office_name': office_name,
        'acronym': acronym,
        'logo': logo,
        'searched': searched,
    }
    return render(request, 'search-organization.html', context)

def view_org(request, org_id,*args, **kwargs):
    
    #set GeneralInformation
    info = GeneralInformation.objects.all()[:1]
    for inf in info:
        office_name = inf.office_name
        acronym = inf.name_acronym
        logo = inf.logo
    
    #get Org
    
    org = Organization.objects.get(pk=org_id)
   
    #get Org db contexts
    #1 events
    events = Event.objects.filter(src_ID = org_id)[:3]
    
    context ={
        'office_name': office_name,
        'acronym': acronym,
        'logo': logo,
        'org': org,
        'events': events,
    }
    return render(request, 'selected-org.html', context)

def view_org_gallery(request,org_id, *args, **kwargs):
     
    #title
    title ="Organizations | BulSUan Kawing"
    
    #set GeneralInformation
    info = GeneralInformation.objects.all()[:1]
    for inf in info:
        office_name = inf.office_name
        acronym = inf.name_acronym
        logo = inf.logo
    #get Org
    org = Organization.objects.get(pk=org_id)
    
    #get Gallery
    albums = Album.objects.filter(src_ID = org_id).order_by('-last_modified')[:4]
    

    context ={
        'title': title,
        'office_name': office_name,
        'acronym': acronym,
        'logo': logo,
        'org': org,
        'albums': albums,
    }
    return render(request, 'org/gallery.html', context)

def view_org_album(request, org_id, album_id, *args, **kwargs):
     
    #title
    title ="Organizations | BulSUan Kawing"
    
    #set GeneralInformation
    info = GeneralInformation.objects.all()[:1]
    for inf in info:
        office_name = inf.office_name
        acronym = inf.name_acronym
        logo = inf.logo
    #get Org
    org = Organization.objects.get(pk=org_id)
    
    #get Album
    album = Album.objects.get(pk = album_id)
    
    #get Album Images
    images = Image.objects.filter(album = album_id)
    context ={
        'title': title,
        'office_name': office_name,
        'acronym': acronym,
        'logo': logo,
        'org': org,
        'images': images,
        'album': album,
    }
    
    return render(request, 'org/album.html', context)
    
def view_org_events (request, org_id, *args, **kwargs):
     #title
    title ="Events | BulSUan Kawing"
    
 
    #get Org
    org = Organization.objects.get(pk= org_id)
    
    #events of org and components
    if request.method =="POST":
        searched = request.POST['searched']
        
        events_list = Event.objects.filter(src_ID = org_id,state__status='Approved')
        events_list = events_list.filter(Q(title__contains=searched)
                           |Q(src_ID__acronym__contains=searched)
                           |Q(src_ID__name__contains = searched)
                           )
    else:
        events_list = Event.objects.filter(src_ID = org_id, state__status='Approved')
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
        'org_id':org_id,
        'events': events,
    }
    return render(request, 'org/events/events.html', context)

def view_org_event(request, org_id=None,event_id=None):
    #get Org
    org = Organization.objects.get(pk=org_id)
    
    #get Event
    event = Event
    if event_id:
        event = get_object_or_404(Event, pk=event_id)
    else:
        event = Event
    

    title = event.title
    context={
        'title': title,
        'event':event,
        'org': org,
        'org_id':org_id,
    }
    return render(request, 'org/events/event-view.html', context)

#OSOA Calendar
class OSOCalendarView(generic.ListView):
    model = Event
    template_name = 'articles/cal/calendar.html'
    
    def get_context_data(self ,**kwargs):
        context = super().get_context_data(**kwargs)
        #import kwargs values
        #set GeneralInformation
        info = GeneralInformation.objects.all()[:1]
        
        for inf in info:
            office_name = inf.office_name
            acronym = inf.name_acronym
            logo = inf.logo
        context ['office_name'] = mark_safe(office_name)
        context ['acronym'] = mark_safe(acronym)
        context ['logo'] = mark_safe(logo)
        


        context['title'] = mark_safe("OSOA Calendar of Events")
        
        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))

        # Instantiate calendar class with today's year and date
        cal = Calendar(d.year, d.month)
        
        # Call the formatmonth method, which returns our calendar as a table
        eventview=1 #event view only level
        html_cal = cal.formatmonth(False,eventview,withyear=True)
        context['calendar'] = mark_safe(html_cal)

        # call previous or next month
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        
        

        return context
    

#Organizational Calendar
class CalendarView(generic.ListView):
    model = Event
    template_name = 'org/cal/calendar.html'
    
    def get_context_data(self ,**kwargs):
        context = super().get_context_data(**kwargs)
        #import kwargs values
        org = Organization.objects.get(pk=self.kwargs['org_id'])
        context['org_id']=mark_safe(self.kwargs['org_id'])
        context['org'] = org
        context['title'] = mark_safe(org.acronym+" Events")
        
        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))

        # Instantiate calendar class with today's year and date
        cal = Calendar(d.year, d.month)
        
        # Call the formatmonth method, which returns our calendar as a table
        eventview=0 #event view only level
        html_cal = cal.formatmonth(self.kwargs['org_id'],eventview,withyear=True)
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

