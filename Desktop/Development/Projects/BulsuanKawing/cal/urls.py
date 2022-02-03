from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'cal'
urlpatterns = [
    path('', views.CalendarView.as_view(), name="calendar"),
    url('event/new/', views.create_event, name='event_new'),
    url('event/edit/(?P<event_id>\d+)/', views.view_event, name='event_edit'),
]
