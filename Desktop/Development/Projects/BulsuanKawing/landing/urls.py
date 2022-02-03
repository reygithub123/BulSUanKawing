from django.urls import path
from events.models import Event

from . import views
app_name = 'landing'
urlpatterns = [
    path('', views.view_homepage, name='view-homepage'),
    path('bulsuankawing/', views.view_about_bk, name ='view-bulsuankawing'),
    path('calendar/', views.OSOCalendarView.as_view(), name ='view-oso-calendar'),
    path('events/', views.view_events, name ='view-oso-events'),
    path('events/<int:event_id>', views.view_event, name ='view-oso-event-desc'),
    path('gallery/', views.view_gallery, name ='view-gallery'),
    path('gallery/<int:album_id>/', views.view_album, name ='view-album'),
    path('news/', views.view_news, name ='view-news'),
    path('news/<int:news_id>/', views.view_news_info, name ='view-news-info'),
    path('organizations/', views.view_search, name='search-org'),
    path('organizations/<int:org_id>/', views.view_org, name='view-org'),
    path('organizations/<int:org_id>/calendar', views.CalendarView.as_view(), name ='view-calendar'),
    path('organizations/<int:org_id>/events', views.view_org_events, name ='view-events'),
    path('organizations/<int:org_id>/event/<int:event_id>', views.view_org_event, name ='view-event-desc'),
    path('organizations/<int:org_id>/gallery/', views.view_org_gallery, name='view-org-gallery'),
    path('organizations/<int:org_id>/gallery/<int:album_id>/', views.view_org_album, name='view-org-album'),
    path('osoa/', views.view_about_oso),
    
    
]
